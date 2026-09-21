from datetime import date, datetime, time

from pymongo import MongoClient
from flask_login import LoginManager

login_manager = LoginManager()


class _Type:
    def __init__(self, *args, **kwargs):
        pass


class STRING(_Type):
    pass


class TEXT(_Type):
    pass


class INTEGER(_Type):
    pass


class BOOLEAN(_Type):
    pass


class DATE(_Type):
    pass


class TIME(_Type):
    pass


class DATETIME(_Type):
    pass


class Field:
    def __init__(self, name=None, field_type=STRING, default=None, nullable=True, **kwargs):
        self.name = name
        self.type = field_type() if isinstance(field_type, type) else field_type
        self.default = default
        self.nullable = nullable

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def ilike(self, pattern):
        text = pattern.strip("%").lower()
        return lambda document: text in str(document.get(self.name, "")).lower()

    def asc(self):
        return self.name, False

    def desc(self):
        return self.name, True


class ColumnCollection:
    def __init__(self, fields):
        self._fields = fields

    def __iter__(self):
        return iter(self._fields.values())


class Table:
    def __init__(self, fields):
        self.columns = ColumnCollection(fields)


class Query:
    def __init__(self, model, documents=None):
        self.model = model
        self.documents = documents

    def _loaded(self):
        if self.documents is None:
            return list(self.model._collection().find())
        return list(self.documents)

    def filter(self, *conditions):
        return Query(self.model, [
            document for document in self._loaded()
            if all(condition(document) for condition in conditions)
        ])

    def filter_by(self, **values):
        return Query(self.model, [
            document for document in self._loaded()
            if all(document.get(key) == value for key, value in values.items())
        ])

    def order_by(self, *sorts):
        documents = list(self._loaded())
        for sort in reversed(sorts):
            field_name, descending = sort if isinstance(sort, tuple) else (sort.name, False)
            documents.sort(
                key=lambda item: (item.get(field_name) is None, item.get(field_name)),
                reverse=descending,
            )
        return Query(self.model, documents)

    def limit(self, amount):
        return Query(self.model, self._loaded()[:amount])

    def all(self):
        return [self.model._from_document(document) for document in self._loaded()]

    def first(self):
        items = self.limit(1).all()
        return items[0] if items else None

    def count(self):
        return len(self._loaded())

    def get(self, item_id):
        document = self.model._collection().find_one({"id": int(item_id)})
        return self.model._from_document(document)


class Session:
    def __init__(self):
        self.pending = []
        self.loaded = []
        self.deleted = []

    def add(self, item):
        if item not in self.pending and item not in self.loaded:
            self.pending.append(item)

    def add_all(self, items):
        for item in items:
            self.add(item)

    def delete(self, item):
        if item not in self.deleted:
            self.deleted.append(item)

    def get(self, model, item_id):
        item = model.query.get(item_id)
        if item and item not in self.loaded:
            self.loaded.append(item)
        return item

    def flush(self):
        for item in self.pending:
            item._ensure_id()

    def commit(self):
        self.flush()
        for item in self.pending + self.loaded:
            item._save()
        for item in self.deleted:
            item.__class__._collection().delete_one({"id": item.id})
        self.pending.clear()
        self.loaded.clear()
        self.deleted.clear()

    def rollback(self):
        self.pending.clear()
        self.loaded.clear()
        self.deleted.clear()


class MongoModel:
    query = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = {
            name: value for name, value in cls.__dict__.items()
            if isinstance(value, Field)
        }
        for name, field in fields.items():
            field.name = name
        cls._fields = fields
        cls.__table__ = Table(fields)
        cls.query = Query(cls)

    def __init__(self, **values):
        for name, field in self._fields.items():
            value = values.get(name, field.default() if callable(field.default) else field.default)
            setattr(self, name, value)
        self._document_id = values.get("_document_id")

    @classmethod
    def _collection(cls):
        return db.connect()[cls.__tablename__]

    @classmethod
    def _from_document(cls, document):
        if document is None:
            return None
        values = dict(document)
        values["_document_id"] = values.pop("_id", None)
        for name, field in cls._fields.items():
            value = values.get(name)
            if not isinstance(value, str):
                continue
            if isinstance(field.type, DATE):
                values[name] = date.fromisoformat(value)
            elif isinstance(field.type, TIME):
                values[name] = time.fromisoformat(value)
            elif isinstance(field.type, DATETIME):
                values[name] = datetime.fromisoformat(value)
        return cls(**values)

    def _ensure_id(self):
        if getattr(self, "id", None) is None:
            latest = self.__class__._collection().find_one(sort=[("id", -1)])
            self.id = (latest.get("id", 0) if latest else 0) + 1

    def _save(self):
        self._ensure_id()
        document = {name: getattr(self, name) for name in self._fields}
        document["id"] = self.id
        for name, value in document.items():
            if isinstance(value, (date, time, datetime)):
                document[name] = value.isoformat()
        self.__class__._collection().replace_one({"id": self.id}, document, upsert=True)


class MongoDatabase:
    Model = MongoModel
    String = STRING
    Text = TEXT
    Integer = INTEGER
    Boolean = BOOLEAN
    Date = DATE
    Time = TIME
    DateTime = DATETIME
    Column = staticmethod(lambda field_type, *args, **kwargs: Field(None, field_type, **kwargs))
    ForeignKey = staticmethod(lambda value: value)
    backref = staticmethod(lambda *args, **kwargs: None)

    def __init__(self):
        self.client = None
        self.database = None
        self.session = Session()

    def init_app(self, app):
        self.uri = app.config["MONGO_URI"]
        self.database_name = app.config["MONGO_DB_NAME"]

    def connect(self):
        if self.database is None:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[self.database_name]
        return self.database

    def create_all(self):
        self.connect()

    @staticmethod
    def relationship(model, **kwargs):
        def related(instance):
            from . import models
            related_model = getattr(models, model)
            return related_model.query.filter_by(id=getattr(instance, f"{model.lower()}_id", None)).first()
        return property(related)


def or_(*conditions):
    return lambda document: any(condition(document) for condition in conditions)


db = MongoDatabase()
