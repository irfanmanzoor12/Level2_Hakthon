from app.database import engine
from sqlmodel import SQLModel, text

# Drop existing tables
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    conn.commit()
    print("✅ Dropped old tables")

# Create new tables with correct schema
SQLModel.metadata.create_all(engine)
print("✅ Created new tables with correct schema")
print("\nDatabase is ready! Restart backend now.")
