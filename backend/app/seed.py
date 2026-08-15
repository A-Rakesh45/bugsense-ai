import os
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.bug import Bug
from app.schemas.auth import UserCreate
from app.schemas.bug import BugCreate
from app.services.auth_service import register_user
from app.services.bug_service import create_bug_with_ai

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if users exist
        if db.query(User).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding initial users...")
        admin = register_user(db, UserCreate(username="admin", email="admin@bugsense.ai", password="password123", role="Admin"))
        tester = register_user(db, UserCreate(username="tester", email="tester@bugsense.ai", password="password123", role="Tester"))
        developer = register_user(db, UserCreate(username="developer", email="dev@bugsense.ai", password="password123", role="Developer"))

        print(f"Users created:\n - Admin: admin / password123\n - Tester: tester / password123\n - Developer: developer / password123")

        print("Seeding initial sample bugs with AI predictions...")
        sample_bugs = [
            BugCreate(
                title="SQL Injection in auth header token parser",
                description="Unsanitized authorization bearer token header allows unauthenticated SQL commands to execute against the MySQL user table.",
                steps_to_reproduce="1. Send GET /api/auth/me with crafted Authorization header\n2. Observe raw SQL exception trace",
                expected_result="Input should be parameterized and reject special characters",
                actual_result="Executes SQL payload and returns administrative session details",
                environment="Production",
                module="Security"
            ),
            BugCreate(
                title="Payment gateway timeout during checkout under concurrency",
                description="Database pool deadlocks during parallel order debit calls under high load, causing HTTP 500 error for customer checkout.",
                steps_to_reproduce="1. Add item to cart\n2. Trigger concurrent POST /api/checkout\n3. Observe pool timeout",
                expected_result="Atomic transaction lock handles order safely",
                actual_result="Database connection pool exhausted; transaction aborts",
                environment="Production",
                module="Payment"
            ),
            BugCreate(
                title="High CPU spikes during monthly PDF report generation",
                description="Exporting financial reports for 10,000+ line items causes RAM memory to exceed 4GB and triggers OOM process termination.",
                steps_to_reproduce="1. Navigate to Reports view\n2. Select Date Range: Full Year\n3. Click Download PDF",
                expected_result="Report streams in chunks without exceeding 500MB RAM",
                actual_result="Worker node crashes with OutOfMemory error",
                environment="Staging",
                module="Performance"
            ),
            BugCreate(
                title="Filter dropdown does not clear active selections on reset button click",
                description="Clicking the Reset Filters button clears search input text but leaves severity dropdown option active in table view.",
                steps_to_reproduce="1. Filter table by Severity = High\n2. Click Reset\n3. Check table rows",
                expected_result="Filter dropdowns return to default 'All' state",
                actual_result="Severity dropdown remains stuck on 'High'",
                environment="Development",
                module="UI/UX"
            ),
            BugCreate(
                title="Typo in assigned bug notification email subject header",
                description="Email notification subject sent to developers reads 'Bug Assignned to You' with spelling mistake.",
                steps_to_reproduce="1. Assign bug to developer\n2. Check inbox notification subject line",
                expected_result="Subject line should read 'Bug Assigned to You'",
                actual_result="Subject contains typo 'Assignned'",
                environment="Development",
                module="General"
            )
        ]

        for b_in in sample_bugs:
            create_bug_with_ai(db, b_in, tester.id)

        print("Database seeding completed successfully with 5 sample AI-analyzed bugs!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
