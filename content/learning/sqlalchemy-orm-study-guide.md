# SQLAlchemy ORM Study Guide

Created: 2026-02-10

---

## What is SQLAlchemy?

SQLAlchemy is Python's most popular database toolkit. It has two layers:

- **Core** — Low-level SQL expression language. You write SQL-like code in Python. Think of it as a programmatic way to build SQL queries without writing raw SQL strings.
- **ORM** (Object-Relational Mapper) — Higher-level layer built on Core. Maps Python classes to database tables. You work with objects instead of rows.

### Core vs ORM Example

**Core approach:**
```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///mydb.db")
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users WHERE age > :age"), {"age": 25})
    for row in result:
        print(row.name, row.age)
```

**ORM approach:**
```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    users = session.query(User).filter(User.age > 25).all()
    for user in users:
        print(user.name, user.age)
```

---

## Key Concepts

### 1. Engine

The starting point. Creates a connection pool to your database.

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost/mydb")
```

- The connection string format: `dialect://user:password@host/database`
- Common dialects: `sqlite`, `postgresql`, `mysql`
- The engine doesn't connect immediately — it's lazy

### 2. Declarative Base

The foundation for defining ORM models. All your model classes inherit from it.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

### 3. Models (Table Mapping)

A Python class that maps to a database table. Each attribute maps to a column.

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    age: Mapped[int | None] = mapped_column(default=None)  # nullable

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
```

Key points:
- `__tablename__` sets the actual table name in the database
- `Mapped[type]` declares the Python type (new style, SQLAlchemy 2.0+)
- `mapped_column()` configures the column (primary key, unique, default, etc.)
- `Mapped[int | None]` makes a column nullable

### 4. Session

The Session is how you interact with the database through the ORM. It:
- Manages a **transaction** (group of operations that succeed or fail together)
- **Tracks changes** to objects (knows what's new, modified, deleted)
- **Flushes** changes to the database (sends SQL)
- **Commits** the transaction (makes changes permanent)

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    # Create
    new_user = User(name="Matt", email="matt@example.com")
    session.add(new_user)
    session.commit()

    # Read
    user = session.query(User).filter_by(name="Matt").first()

    # Update
    user.name = "Matthew"
    session.commit()

    # Delete
    session.delete(user)
    session.commit()
```

### 5. Querying (SQLAlchemy 2.0 Style)

The modern way uses `select()`:

```python
from sqlalchemy import select

with Session(engine) as session:
    # Get all users
    stmt = select(User)
    users = session.scalars(stmt).all()

    # Filter
    stmt = select(User).where(User.age > 25)
    users = session.scalars(stmt).all()

    # Order
    stmt = select(User).order_by(User.name)

    # Limit
    stmt = select(User).limit(10)

    # Get one or None
    user = session.scalars(select(User).where(User.id == 1)).first()
```

### 6. Relationships

Link tables together using foreign keys and `relationship()`.

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

- `ForeignKey("users.id")` creates the database-level link
- `relationship()` creates the Python-level access (user.posts, post.author)
- `back_populates` keeps both sides in sync

### 7. The N+1 Problem

A common performance trap with ORMs.

**The problem:** Loading a user's posts triggers a separate query per user.
```python
users = session.scalars(select(User)).all()
for user in users:
    print(user.posts)  # Each iteration = another SQL query!
```

If you have 100 users, that's 1 + 100 = 101 queries.

**The solution:** Eager loading — load related data upfront.
```python
from sqlalchemy.orm import joinedload, selectinload

# joinedload: single query with JOIN
stmt = select(User).options(joinedload(User.posts))

# selectinload: two queries (one for users, one for all their posts using IN)
stmt = select(User).options(selectinload(User.posts))
```

### 8. Creating Tables

```python
# Create all tables defined by models inheriting from Base
Base.metadata.create_all(engine)

# Drop all tables (careful!)
Base.metadata.drop_all(engine)
```

---

## Common Patterns

### Session as Context Manager
```python
with Session(engine) as session:
    with session.begin():  # auto-commits or rolls back
        session.add(User(name="Matt"))
    # transaction committed here if no exception
```

### Sessionmaker (Reusable Session Factory)
```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

# Usage
with SessionLocal() as session:
    ...
```

### FastAPI + SQLAlchemy (Dependency Injection)
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()
```

---

## Quick Reference

| Operation | Code |
|-----------|------|
| Create engine | `create_engine("postgresql://user:pass@host/db")` |
| Define model | `class User(Base): __tablename__ = "users"` |
| Add record | `session.add(obj)` then `session.commit()` |
| Query all | `session.scalars(select(User)).all()` |
| Filter | `select(User).where(User.name == "Matt")` |
| Update | Modify the object, then `session.commit()` |
| Delete | `session.delete(obj)` then `session.commit()` |
| Eager load | `select(User).options(joinedload(User.posts))` |
| Create tables | `Base.metadata.create_all(engine)` |

---

## What I'll Quiz You On

1. Core vs ORM — what's the difference?
2. What is a Session and what does it do?
3. Define a model with mapped_column
4. The N+1 problem — what is it and how do you fix it?

---

*Study guide created by MARVIN for spaced repetition review*
