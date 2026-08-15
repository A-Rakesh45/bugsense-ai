import csv
import random
import os

MODULES = [
    "Authentication", "Payment", "Database", "Network", 
    "UI/UX", "Performance", "Integration", "Security", "General"
]

SEVERITIES = ["Critical", "High", "Medium", "Low"]
PRIORITIES = ["P1", "P2", "P3", "P4"]
CATEGORIES = [
    "Functional", "UI/UX", "Performance", "Security", "Database", 
    "Network", "Authentication", "Payment", "Integration", "Other"
]

ENVIRONMENTS = ["Production", "Staging", "Development"]

BUG_TEMPLATES = [
    # Critical / P1 / Security / Payment / Auth
    {
        "title": "SQL Injection vulnerability in user login input field",
        "description": "Unsanitized user input in the username field allows unauthenticated SQL injection attacks against the authentication database, bypassing login checks.",
        "steps": "1. Navigate to /auth/login\n2. Enter ' OR '1'='1 in username field\n3. Submit form",
        "expected": "Input should be sanitized or rejected with validation error",
        "actual": "Bypasses password verification and logs in as admin user",
        "severity": "Critical",
        "priority": "P1",
        "category": "Security",
        "module": "Authentication"
    },
    {
        "title": "Payment gateway deadlock during concurrent checkout transactions",
        "description": "Double debit occurring during concurrent payment processing under peak load. Database connection pool gets exhausted and throws 500 error.",
        "steps": "1. Add items to cart\n2. Trigger concurrent checkout API calls simultaneously\n3. Observe database connection timeout",
        "expected": "Transaction locks should prevent race conditions and execute atomically",
        "actual": "Payment fails with 500 Internal Server Error and user is debited twice",
        "severity": "Critical",
        "priority": "P1",
        "category": "Payment",
        "module": "Payment"
    },
    {
        "title": "Production database connection leak causes full application outage",
        "description": "Database connection pool is not returning connections to pool after long queries, leading to complete API freeze across all endpoints.",
        "steps": "1. Execute 50 heavy reporting queries in parallel\n2. Observe active connection count in database metrics",
        "expected": "Connection pool recycles idle connections cleanly",
        "actual": "Max connection limit exceeded; server hangs indefinitely",
        "severity": "Critical",
        "priority": "P1",
        "category": "Database",
        "module": "Database"
    },
    {
        "title": "Buffer overflow and remote code execution in file upload service",
        "description": "Unchecked image binary buffer allocation causes memory crash and allows arbitrary execution of binary script payloads on production nodes.",
        "steps": "1. Upload corrupted binary file with executable headers to /api/upload\n2. Trigger file processing daemon",
        "expected": "File validator should sanitize file types and reject malicious binaries",
        "actual": "Worker service crashes immediately with core dump",
        "severity": "Critical",
        "priority": "P1",
        "category": "Security",
        "module": "Security"
    },
    # High / P2 / Performance / Integration / Network
    {
        "title": "High CPU utilization and memory leak during PDF report generation",
        "description": "Exporting monthly financial reports causes worker process memory to spike from 250MB to 4GB, forcing OOM killer to terminate service.",
        "steps": "1. Go to Reports module\n2. Select Date Range: Last 12 months\n3. Click Export to PDF",
        "expected": "PDF stream generation should execute within 500MB memory footprint",
        "actual": "Worker node consumes 100% CPU and crashes with OutOfMemoryError",
        "severity": "High",
        "priority": "P2",
        "category": "Performance",
        "module": "Performance"
    },
    {
        "title": "OAuth SSO callback fails with invalid state token error",
        "description": "Single Sign-On authentication fails intermittently for Google and Azure AD users due to session cookie mismatch across load balancers.",
        "steps": "1. Click Login with SSO\n2. Complete third-party login\n3. Redirect back to application",
        "expected": "SSO session token validated and dashboard loaded",
        "actual": "Redirect loops back to login page with HTTP 403 Invalid State",
        "severity": "High",
        "priority": "P2",
        "category": "Integration",
        "module": "Integration"
    },
    {
        "title": "REST API response time degraded by 300% after database migration",
        "description": "Query execution plan missing composite index on (tenant_id, created_at), causing full table scans on table with 5 million rows.",
        "steps": "1. Fetch list of bugs for tenant using GET /api/bugs\n2. Measure server latency",
        "expected": "API response delivered within 150ms",
        "actual": "Query execution takes 4.8 seconds to respond",
        "severity": "High",
        "priority": "P2",
        "category": "Database",
        "module": "Database"
    },
    {
        "title": "WebSocket live notification stream drops connection every 60 seconds",
        "description": "TCP keep-alive heartbeat ping is not sent by server socket, causing ingress proxy to terminate persistent connections prematurely.",
        "steps": "1. Open live dashboard\n2. Wait 60 seconds without user interaction",
        "expected": "WebSocket connection stays open indefinitely with active ping-pong",
        "actual": "Connection closed unexpectedly with code 1006",
        "severity": "High",
        "priority": "P2",
        "category": "Network",
        "module": "Network"
    },
    # Medium / P3 / Functional / UI/UX
    {
        "title": "Bug filter dropdown does not clear selected values on reset",
        "description": "Clicking the Clear Filters button resets text search inputs but leaves selected severity dropdown option active in table state.",
        "steps": "1. Select Severity = High\n2. Click Clear Filters button\n3. Observe table rows",
        "expected": "All filter dropdowns reset to default All state",
        "actual": "Dropdown still displays High and table remains filtered",
        "severity": "Medium",
        "priority": "P3",
        "category": "UI/UX",
        "module": "UI/UX"
    },
    {
        "title": "Incorrect pagination count on bug list view",
        "description": "Pagination footer displays 'Showing 1-10 of 45' even when total count is updated to 120 items after applying search query.",
        "steps": "1. Search for keyword 'payment'\n2. Navigate to page 2",
        "expected": "Total item counter updates dynamically to match filtered subset",
        "actual": "Footer displays stale total item count from unfiltered query",
        "severity": "Medium",
        "priority": "P3",
        "category": "Functional",
        "module": "General"
    },
    {
        "title": "Export CSV feature truncates descriptions containing commas",
        "description": "Generated CSV file does not wrap text fields in double quotes, causing spreadsheet software to split description text across multiple columns.",
        "steps": "1. Create bug with description containing commas\n2. Click Export to CSV\n3. Open file in Excel",
        "expected": "Text fields properly escaped according to RFC 4180 standard",
        "actual": "Comma splits text into adjacent data columns, distorting rows",
        "severity": "Medium",
        "priority": "P3",
        "category": "Functional",
        "module": "General"
    },
    {
        "title": "User avatar image fails to load on profile header",
        "description": "Broken image link placeholder displayed when avatar URL returns HTTP 404 from CDN endpoint.",
        "steps": "1. Log into portal\n2. Check upper right corner avatar icon",
        "expected": "User initial avatar fallback renders when image fails to load",
        "actual": "Broken image icon rendered with missing alt text",
        "severity": "Medium",
        "priority": "P3",
        "category": "UI/UX",
        "module": "UI/UX"
    },
    # Low / P4 / Other / Cosmetic
    {
        "title": "Typo in email notification subject header",
        "description": "Notification email sent upon bug assignment contains spelling error in subject line: 'Bug Assignned to You'.",
        "steps": "1. Assign bug to developer\n2. Check inbox notification email",
        "expected": "Subject reads 'Bug Assigned to You'",
        "actual": "Subject contains double 'n' typo",
        "severity": "Low",
        "priority": "P4",
        "category": "Other",
        "module": "General"
    },
    {
        "title": "Footer copyright year displays outdated date 2023",
        "description": "Static footer component renders hardcoded copyright text instead of dynamically reading current calendar year.",
        "steps": "1. Scroll to bottom of dashboard landing page\n2. Inspect footer text",
        "expected": "Copyright displays current year © 2026",
        "actual": "Copyright displays hardcoded © 2023",
        "severity": "Low",
        "priority": "P4",
        "category": "UI/UX",
        "module": "UI/UX"
    },
    {
        "title": "Tooltips on table column headers missing accessibility aria-labels",
        "description": "Hovering over column headers shows tooltip text, but screen readers do not read description for assistive technology users.",
        "steps": "1. Inspect header elements using DevTools accessibility audit\n2. Check aria-describedby attribute",
        "expected": "Accessible label bound to tooltip popup",
        "actual": "Missing aria attributes on SVG icon container",
        "severity": "Low",
        "priority": "P4",
        "category": "UI/UX",
        "module": "UI/UX"
    }
]

VARIANTS = [
    "observed in staging deployment", "during load test run", "after v1.4 patch release",
    "on mobile Safari browser", "under high concurrent traffic", "on Kubernetes cluster node 3",
    "intermittently after session timeout", "when running background cron job", "in microservice container"
]

def generate_dataset(file_path: str, count: int = 1200):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    rows = []
    for i in range(count):
        tmpl = random.choice(BUG_TEMPLATES)
        variant = random.choice(VARIANTS)
        
        # Inject minor realistic variation into title and description
        title = f"{tmpl['title']} ({variant})"
        description = f"{tmpl['description']} Note: Issue was reported {variant}."
        
        rows.append({
            "title": title,
            "description": description,
            "steps_to_reproduce": tmpl["steps"],
            "expected_result": tmpl["expected"],
            "actual_result": tmpl["actual"],
            "environment": random.choice(ENVIRONMENTS),
            "module": tmpl["module"],
            "severity": tmpl["severity"],
            "priority": tmpl["priority"],
            "category": tmpl["category"]
        })
        
    fieldnames = [
        "title", "description", "steps_to_reproduce", "expected_result", 
        "actual_result", "environment", "module", "severity", "priority", "category"
    ]
    
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Dataset successfully created with {count} bug records at {file_path}")

if __name__ == "__main__":
    output_csv = os.path.join(os.path.dirname(__file__), "bug_dataset.csv")
    generate_dataset(output_csv, 1200)
