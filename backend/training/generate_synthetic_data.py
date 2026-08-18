import csv
import random
import os

MODULES = [
    "Authentication", "Payment", "Database", "Network", 
    "UI/UX", "Performance", "Integration", "Security", "General"
]

ENVIRONMENTS = ["Production", "Staging", "Development"]

# Distinct, high-precision domain templates for all 10 Categories across all Severities and Priorities
FINE_TEMPLATES = [
    # SECURITY
    {
        "category": "Security", "severity": "Critical", "priority": "P1", "module": "Security",
        "title": "SQL Injection security vulnerability in login authentication field",
        "description": "Unsanitized user input in security field allows unauthenticated SQL injection exploit against user database.",
        "expected": "Security input sanitization and SQL parameterization should block injection payload",
        "actual": "Security authentication check bypassed allowing unauthorized access"
    },
    {
        "category": "Security", "severity": "High", "priority": "P2", "module": "Security",
        "title": "Cross-Site Scripting XSS security vulnerability in comment box",
        "description": "Stored XSS security vulnerability executes arbitrary JavaScript in victim browser session.",
        "expected": "Security HTML tag escaping should sanitize XSS payload",
        "actual": "Malicious XSS script tag executes on profile page"
    },
    {
        "category": "Security", "severity": "Medium", "priority": "P3", "module": "Security",
        "title": "Missing security HTTP Content-Security-Policy headers",
        "description": "Application security response headers lack CSP protection against frame injection.",
        "expected": "Include security response headers CSP and X-Frame-Options",
        "actual": "Security response headers missing CSP directives"
    },
    {
        "category": "Security", "severity": "Low", "priority": "P4", "module": "Security",
        "title": "Verbose server header leaks proxy security version info",
        "description": "HTTP Server security response header reveals backend proxy version string.",
        "expected": "Mask security server version strings in production",
        "actual": "Header leaks Server version information"
    },

    # PAYMENT
    {
        "category": "Payment", "severity": "Critical", "priority": "P1", "module": "Payment",
        "title": "Payment gateway deadlock causing duplicate debit charge",
        "description": "Concurrent payment checkout requests cause deadlock resulting in double credit card debit.",
        "expected": "Atomic payment transaction lock prevents duplicate charges",
        "actual": "Payment fails with 500 error and debits customer twice"
    },
    {
        "category": "Payment", "severity": "High", "priority": "P2", "module": "Payment",
        "title": "Stripe payment API webhook notification signature failure",
        "description": "Asynchronous payment gateway notification webhook drops checkout completion events.",
        "expected": "Validate Stripe payment webhook signature correctly",
        "actual": "Payment status remains pending after credit card charge"
    },
    {
        "category": "Payment", "severity": "Medium", "priority": "P3", "module": "Payment",
        "title": "Currency symbol display mismatch in checkout payment summary",
        "description": "Payment conversion calculates correctly but displays wrong currency symbol prefix.",
        "expected": "Display correct currency symbol on payment screen",
        "actual": "Displays $ instead of EUR symbol for payment total"
    },
    {
        "category": "Payment", "severity": "Low", "priority": "P4", "module": "Payment",
        "title": "Saved payment card mask displays 14 visible digits",
        "description": "Credit card payment mask displays 14 visible digits on account billing page.",
        "expected": "Mask all but last 4 payment card numbers",
        "actual": "Payment card digits exposed on screen"
    },

    # DATABASE
    {
        "category": "Database", "severity": "Critical", "priority": "P1", "module": "Database",
        "title": "Database connection pool leak exhausts active DB connections",
        "description": "Unclosed database ORM sessions leak database connection pool capacity causing API crash.",
        "expected": "Recycle idle database connection pool threads automatically",
        "actual": "Database connection pool timeout error"
    },
    {
        "category": "Database", "severity": "High", "priority": "P2", "module": "Database",
        "title": "Missing composite database index causes full table scan",
        "description": "Database query plan performs full table scan on 10 million database rows.",
        "expected": "Execute database query using composite index under 50ms",
        "actual": "Database query latency spikes to 9 seconds"
    },
    {
        "category": "Database", "severity": "Medium", "priority": "P3", "module": "Database",
        "title": "Read replica database synchronization delay lag",
        "description": "Replication lag on secondary database instance returns stale database records.",
        "expected": "Database replication sync delay under 200ms",
        "actual": "Stale database records returned to read query"
    },
    {
        "category": "Database", "severity": "Low", "priority": "P4", "module": "Database",
        "title": "Database migration script outputs deprecated syntax warning",
        "description": "Database schema migration succeeds but logs SQL index syntax warning.",
        "expected": "Clean database migration execution logs",
        "actual": "Deprecated database index syntax warning logged"
    },

    # PERFORMANCE
    {
        "category": "Performance", "severity": "Critical", "priority": "P1", "module": "Performance",
        "title": "Memory leak during PDF export triggers OOM performance crash",
        "description": "Exporting PDF documents consumes 4GB heap RAM memory causing OOM performance killer crash.",
        "expected": "Optimize PDF stream memory allocation under 250MB",
        "actual": "Performance crash with OutOfMemory error"
    },
    {
        "category": "Performance", "severity": "High", "priority": "P2", "module": "Performance",
        "title": "High CPU utilization spike during concurrent CSV file parsing",
        "description": "Parsing 500MB CSV file locks CPU performance threads causing API response lag.",
        "expected": "Process CSV parsing in async background queue to maintain performance",
        "actual": "Server CPU spikes to 100% performance degradation"
    },
    {
        "category": "Performance", "severity": "Medium", "priority": "P3", "module": "Performance",
        "title": "N+1 SQL query loop in list view degrades page load performance",
        "description": "Looping over table records triggers 150 individual SQL queries degrading performance.",
        "expected": "Use eager loading SQL joins for page performance",
        "actual": "150 separate queries degrade load performance"
    },
    {
        "category": "Performance", "severity": "Low", "priority": "P4", "module": "Performance",
        "title": "Unused JavaScript bundle assets increase page load time",
        "description": "Legacy library dependencies included in main production bundle slowing performance.",
        "expected": "Tree-shake unused script files for optimal frontend performance",
        "actual": "Bundle size 50KB larger than optimal performance benchmark"
    },

    # AUTHENTICATION
    {
        "category": "Authentication", "severity": "Critical", "priority": "P1", "module": "Authentication",
        "title": "Multi-Factor Authentication MFA bypass via direct login route",
        "description": "Navigating directly to protected URL skips mandatory MFA passcode prompt during authentication.",
        "expected": "Enforce MFA authentication before issuing access token",
        "actual": "Bypasses authentication MFA verification check"
    },
    {
        "category": "Authentication", "severity": "High", "priority": "P2", "module": "Authentication",
        "title": "OAuth2 SSO authentication callback loop state mismatch",
        "description": "Single Sign-On SSO authentication redirect fails for Azure AD login users.",
        "expected": "Validate SSO authentication state token cleanly",
        "actual": "Authentication redirect loop with 403 error"
    },
    {
        "category": "Authentication", "severity": "Medium", "priority": "P3", "module": "Authentication",
        "title": "Password reset token does not expire after single redemption",
        "description": "Password reset link remains active for authentication multiple times.",
        "expected": "Invalidate password reset token after single authentication use",
        "actual": "Reset token re-usable for 24 hours"
    },
    {
        "category": "Authentication", "severity": "Low", "priority": "P4", "module": "Authentication",
        "title": "Login form password input field missing autocomplete attribute",
        "description": "Password manager browser extension fails to auto-fill authentication password field.",
        "expected": "Set autocomplete='current-password' for authentication UX",
        "actual": "Password manager fails to detect field"
    },

    # NETWORK
    {
        "category": "Network", "severity": "Critical", "priority": "P1", "module": "Network",
        "title": "HTTP 504 Gateway Timeout on microservice network proxy",
        "description": "Network API gateway proxy drops inbound requests taking longer than 30 seconds.",
        "expected": "Maintain network proxy connection for long requests",
        "actual": "Network proxy returns 504 Gateway Timeout"
    },
    {
        "category": "Network", "severity": "High", "priority": "P2", "module": "Network",
        "title": "WebSocket live stream network connection drops every 60 seconds",
        "description": "Missing network ping heartbeat ping causes reverse proxy to terminate socket connection.",
        "expected": "Send periodic WebSocket network keep-alive ping",
        "actual": "Network socket connection closes with code 1006"
    },
    {
        "category": "Network", "severity": "Medium", "priority": "P3", "module": "Network",
        "title": "CORS preflight network request fails on custom HTTP headers",
        "description": "OPTIONS network request returns 403 Forbidden due to missing Access-Control header.",
        "expected": "Allow custom headers in CORS network handler",
        "actual": "Browser blocks cross-origin network API request"
    },
    {
        "category": "Network", "severity": "Low", "priority": "P4", "module": "Network",
        "title": "DNS lookup retry delay adds 150ms latency to network calls",
        "description": "Secondary DNS network resolver lookup retries before resolving hostname.",
        "expected": "Fast primary DNS network resolution under 10ms",
        "actual": "Intermittent 150ms network delay"
    },

    # UI/UX
    {
        "category": "UI/UX", "severity": "Critical", "priority": "P1", "module": "UI/UX",
        "title": "Modal dialog close button unclickable on mobile viewport UI/UX",
        "description": "Modal close button positioned outside viewport UI/UX touch boundary.",
        "expected": "Responsive UI/UX modal bounds with accessible tap target",
        "actual": "User stuck on modal UI/UX screen"
    },
    {
        "category": "UI/UX", "severity": "High", "priority": "P2", "module": "UI/UX",
        "title": "Filter dropdown selected values fail to clear on reset UI/UX click",
        "description": "Clicking Clear Filters resets text but leaves dropdown selection active in UI/UX state.",
        "expected": "Reset all UI/UX filter components to default state",
        "actual": "Dropdown selection remains active in UI/UX state"
    },
    {
        "category": "UI/UX", "severity": "Medium", "priority": "P3", "module": "UI/UX",
        "title": "Dark mode text contrast ratio fails accessibility UI/UX guidelines",
        "description": "Muted gray text on dark background has insufficient contrast ratio in UI/UX theme.",
        "expected": "Maintain WCAG AAA contrast ratio 4.5:1 for UI/UX",
        "actual": "Text illegible in dark UI/UX theme"
    },
    {
        "category": "UI/UX", "severity": "Low", "priority": "P4", "module": "UI/UX",
        "title": "User avatar image renders broken placeholder icon on CDN UI/UX 404",
        "description": "Broken image icon rendered when user profile picture URL fails in UI/UX.",
        "expected": "Render fallback initial avatar icon in UI/UX",
        "actual": "Broken image placeholder shown in UI/UX layout"
    },

    # FUNCTIONAL
    {
        "category": "Functional", "severity": "Critical", "priority": "P1", "module": "General",
        "title": "Bulk delete functional action removes wrong record IDs",
        "description": "Select all functional checkbox maps array index instead of database record ID.",
        "expected": "Execute functional deletion on selected database IDs only",
        "actual": "Deletes wrong database records in functional execution"
    },
    {
        "category": "Functional", "severity": "High", "priority": "P2", "module": "General",
        "title": "Incorrect functional pagination item count displayed on table footer",
        "description": "Footer displays total count from unfiltered dataset after applying functional search.",
        "expected": "Update functional item count to match active search filter",
        "actual": "Displays stale total count in table functional footer"
    },
    {
        "category": "Functional", "severity": "Medium", "priority": "P3", "module": "General",
        "title": "Export CSV functional feature truncates descriptions with commas",
        "description": "CSV functional generator fails to wrap string values in double quotes.",
        "expected": "Escape commas in CSV functional export",
        "actual": "Splits text across columns in functional export"
    },
    {
        "category": "Functional", "severity": "Low", "priority": "P4", "module": "General",
        "title": "Date picker functional filter applies timezone offset incorrectly",
        "description": "Selecting start date converts time to UTC shifting selected functional day.",
        "expected": "Preserve selected date string in functional filter",
        "actual": "Shifts selected date by -1 day in functional query"
    },

    # INTEGRATION
    {
        "category": "Integration", "severity": "Critical", "priority": "P1", "module": "Integration",
        "title": "Zapier webhook integration pipeline drops sync events",
        "description": "Data integration sync pipeline fails to retry dropped HTTP events under failure.",
        "expected": "Guaranteed event delivery across integration pipeline",
        "actual": "Integration sync events silently lost"
    },
    {
        "category": "Integration", "severity": "High", "priority": "P2", "module": "Integration",
        "title": "Third-party REST integration API rate limit returns 429 error",
        "description": "Exceeding vendor API quota throws uncaught integration exception in worker queue.",
        "expected": "Implement exponential backoff retry in integration client",
        "actual": "Integration worker process crashes"
    },
    {
        "category": "Integration", "severity": "Medium", "priority": "P3", "module": "Integration",
        "title": "Jira issue integration sync fails on custom field schema mismatch",
        "description": "Custom field value formatting causes Jira integration REST API validation error.",
        "expected": "Format payload according to Jira integration spec",
        "actual": "Jira integration sync fails"
    },
    {
        "category": "Integration", "severity": "Low", "priority": "P4", "module": "Integration",
        "title": "Slack webhook integration notification fails when title contains quotes",
        "description": "Unescaped double quotes in bug title break Slack integration JSON payload.",
        "expected": "Sanitize JSON payload strings for integration webhook",
        "actual": "Slack integration notification fails"
    },

    # OTHER
    {
        "category": "Other", "severity": "Critical", "priority": "P1", "module": "General",
        "title": "Cron job scheduler thread deadlocks halting automated tasks",
        "description": "Shared lock between scheduled tasks causes task runner service to stall.",
        "expected": "Isolated task execution threads for background jobs",
        "actual": "Cron scheduler completely stops execution"
    },
    {
        "category": "Other", "severity": "High", "priority": "P2", "module": "General",
        "title": "Email notification sender address rejected by SPF DMARC policy",
        "description": "Outbound transaction email missing valid DKIM signature in mail header.",
        "expected": "Send authenticated email headers with DKIM signature",
        "actual": "Notification emails marked as spam"
    },
    {
        "category": "Other", "severity": "Medium", "priority": "P3", "module": "General",
        "title": "Help center documentation search returns 500 on special characters",
        "description": "Searching documentation with quotes throws unhandled server exception.",
        "expected": "Sanitize search input terms in documentation portal",
        "actual": "500 Internal Server Error"
    },
    {
        "category": "Other", "severity": "Low", "priority": "P4", "module": "General",
        "title": "Typo in assignment notification email subject header text",
        "description": "Notification email subject contains spelling error: 'Bug Assignned'.",
        "expected": "Correct spelling: 'Bug Assigned'",
        "actual": "Displays 'Assignned' with double n"
    }
]

VARIANTS = [
    "observed in staging deployment", "during load test run", "after v1.4 patch release",
    "on mobile Safari browser", "under high concurrent traffic", "on Kubernetes cluster node 3",
    "intermittently after session timeout", "when running background cron job", "in microservice container"
]

def generate_dataset(file_path: str, count: int = 1600):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    rows = []
    for i in range(count):
        tmpl = FINE_TEMPLATES[i % len(FINE_TEMPLATES)]
        variant = random.choice(VARIANTS)
        
        title = f"{tmpl['title']} ({variant})"
        description = f"{tmpl['description']} Note: Defect was verified {variant}."
        
        rows.append({
            "title": title,
            "description": description,
            "steps_to_reproduce": f"1. Reproduce: {tmpl['title']}\n2. Observe result {variant}",
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
        
    print(f"High-Precision Balanced Dataset created with {count} records at {file_path}")

if __name__ == "__main__":
    output_csv = os.path.join(os.path.dirname(__file__), "bug_dataset.csv")
    generate_dataset(output_csv, 1600)
