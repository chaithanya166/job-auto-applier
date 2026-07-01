import os
import asyncio
from fastapi import FastAPI, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from playwright.async_api import async_playwright

# Set the permanent storage path for the Playwright browser immediately on startup
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/src/.cache/ms-playwright"

app = FastAPI()

# Setup a local directory to save uploaded resumes
UPLOAD_DIR = "./resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global memory storage for tracking applied jobs
APPLIED_JOBS_TRACKER = []

# ==========================================
# ✅ GLOBAL ADSENSE CODE INJECTED FOR ALL SLOTS
# ==========================================
AD_CODE_SNIPPET = """
<div style="text-align: center; margin: 20px auto; max-width: 100%;">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6042910797679767" crossorigin="anonymous"></script>
    <div style="margin: 5px; color: #6c757d; font-size: 11px; letter-spacing: 1px; font-weight: bold;">SPONSORED ADVERTISEMENT</div>
</div>
"""

# --- ROUTE FOR GOOGLE TO INSTANTLY READ YOUR AUTHORIZED ADS.TXT VALUE ---
@app.get("/ads.txt", response_class=PlainTextResponse)
async def get_ads_txt():
    return "google.com, pub-6042910797679767, DIRECT, f08c47fec0942fa0"

# --- 1. THE SETUP FORM PAGE ---
@app.get("/", response_class=HTMLResponse)
async def main_page():
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>Universal Auto-Applier Setup</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6042910797679767" crossorigin="anonymous"></script>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background-color: #f8f9fa;">
            
            {AD_CODE_SNIPPET} <div style="background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px;">
                <h2 style="margin-top:0; color:#333;">🚀 Universal Job Auto-Applier Setup</h2>
                <p style="color: #666; font-size: 14px;">Fill out your details. Once submitted, monitor the live tracker tab.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin-bottom: 20px;">
                
                <form action="/start-automation" method="post" enctype="multipart/form-data">
                    <h3>Step 1: Your Profile Details</h3>
                    <label>First Name:</label><br><input type="text" name="first_name" required style="width:100%; padding:8px; margin-bottom:10px; box-sizing:border-box;"><br>
                    <label>Last Name:</label><br><input type="text" name="last_name" required style="width:100%; padding:8px; margin-bottom:10px; box-sizing:border-box;"><br>
                    <label>Email Address:</label><br><input type="email" name="email" required style="width:100%; padding:8px; margin-bottom:10px; box-sizing:border-box;"><br>
                    <label>Upload Resume (PDF):</label><br><input type="file" name="resume" accept=".pdf" required style="margin-bottom:20px;"><br>
                    
                    <h3>Step 2: Job Targeting Filters</h3>
                    <label>Job Title Keywords:</label><br>
                    <input type="text" name="keywords" placeholder="QA Tester, Project Coordinator" required style="width:100%; padding:8px; margin-bottom:10px; box-sizing:border-box;"><br>
                    <label>Target Location:</label><br>
                    <input type="text" name="location" placeholder="Remote, United States" required style="width:100%; padding:8px; margin-bottom:20px; box-sizing:border-box;"><br>
                    
                    <button type="submit" style="background: #007bff; color: white; border: none; padding: 12px 20px; cursor: pointer; border-radius: 5px; font-size:16px; width:100%; font-weight: bold;">
                        Start Auto-Apply Process
                    </button>
                </form>
                <br>
                <a href="/tracker" style="display:block; text-align:center; color:#007bff; text-decoration:none;">View Existing Application Tracker →</a>
            </div>

            {AD_CODE_SNIPPET} </body>
    </html>
    """

# --- 2. THE TRACKER DASHBOARD PAGE ---
@app.get("/tracker", response_class=HTMLResponse)
async def tracker_page():
    tracker_rows = ""
    if not APPLIED_JOBS_TRACKER:
        tracker_rows = "<tr><td colspan='4' style='text-align:center; padding:20px; color:#888;'>Job engine initializing... Please give it a brief moment to update.</td></tr>"
    else:
        for index, job in enumerate(APPLIED_JOBS_TRACKER, 1):
            if "Success" in job["status"] or "Found" in job["status"]:
                status_color = "#28a745"
            elif "Initializing" in job["status"] or "Connecting" in job["status"]:
                status_color = "#007bff"
            elif "Skipped" in job["status"]:
                status_color = "#ffc107"
            else:
                status_color = "#dc3545"
                
            tracker_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">{index}</td>
                <td style="padding: 10px;"><strong>{job['title']}</strong></td>
                <td style="padding: 10px;"><a href="{job['url']}" target="_blank" style="color:#007bff; text-decoration:none;">Link</a></td>
                <td style="padding: 10px; color: {status_color}; font-weight: bold;">{job['status']}</td>
            </tr>
            """

    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>Application Tracking Dashboard</title>
            <meta http-equiv="refresh" content="3">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6042910797679767" crossorigin="anonymous"></script>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f8f9fa;">
            <p><a href="/" style="color:#007bff; text-decoration:none;">← Back to Application Form</a></p>
            
            {AD_CODE_SNIPPET} <div style="background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 4px solid #007bff;">
                <h3 style="margin-top:0; color:#333; display: flex; justify-content: space-between; align-items: center;">
                    📋 Live Job Tracking Dashboard
                    <span style="font-size:12px; color:#666; font-weight:normal;">🔄 Auto-updating every 3s</span>
                </h3>
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr style="background-color: #e9ecef; border-bottom: 2px solid #dee2e6;">
                            <th style="padding: 10px; width: 5%;">#</th>
                            <th style="padding: 10px; width: 50%;">Job Role / Keywords Targeted</th>
                            <th style="padding: 10px; width: 25%;">Link</th>
                            <th style="padding: 10px; width: 20%;">Application Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tracker_rows}
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """

# --- 3. THE LIVE CLOUD RUNNER ENGINE ---
async def run_job_automation(user_info: dict, keywords: str, location: str):
    global APPLIED_JOBS_TRACKER
    
    APPLIED_JOBS_TRACKER.append({
        "title": f"Search Setup: {keywords}",
        "url": "#",
        "status": "Initializing Production Browser Engine..."
    })
    
    async with async_playwright() as p:
        try:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/src/.cache/ms-playwright"
            
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()
            
            formatted_keywords = keywords.replace(" ", "%20").replace("&", "%26")
            formatted_location = location.replace(" ", "%20")
            search_url = f"https://www.linkedin.com/jobs/search?keywords={formatted_keywords}&location={formatted_location}"
            
            APPLIED_JOBS_TRACKER[0]["status"] = "Connecting to Platform Indexes..."
            
            await page.goto(search_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            
            job_cards = await page.query_selector_all("a.base-card__full-link, a.job-search-card__url")
            job_urls = []
            
            for card in job_cards[:5]:
                url = await card.get_attribute("href")
                if url:
                    job_urls.append(url.split("?")[0])
            
            if not job_urls:
                APPLIED_JOBS_TRACKER[0]["status"] = "Skipped (Target site requested Verification/CAPTCHA)"
                await browser.close()
                return

            APPLIED_JOBS_TRACKER[0]["status"] = f"Success (Discovered {len(job_urls)} listings)"

            for url in job_urls:
                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)
                    
                    first_name_input = await page.query_selector('input[name*="first"], input[id*="first"]')
                    email_input = await page.query_selector('input[type="email"], input[name*="email"]')
                    
                    if first_name_input and email_input:
                        await page.fill('input[name*="first"]', user_info["first_name"])
                        await page.fill('input[name*="last"]', user_info["last_name"])
                        await page.fill('input[type="email"]', user_info["email"])
                        
                        file_input = await page.query_selector('input[type="file"]')
                        if file_input:
                            async with page.expect_file_chooser() as fc_info:
                                await page.click('input[type="file"]')
                            file_chooser = await fc_info.value
                            await file_chooser.set_files(user_info["resume_path"])
                        
                        APPLIED_JOBS_TRACKER.append({
                            "title": keywords,
                            "url": url,
                            "status": "Success (Details Filled)"
                        })
                    else:
                        APPLIED_JOBS_TRACKER.append({
                            "title": keywords,
                            "url": url,
                            "status": "Skipped (Requires Account Login)"
                        })
                        
                except Exception as inner_e:
                    APPLIED_JOBS_TRACKER.append({
                        "title": keywords,
                        "url": url,
                        "status": f"Page Connection issue"
                    })
            
            await browser.close()
            
        except Exception as e:
            print(f"[Engine Fatal Error]: {str(e)}")
            APPLIED_JOBS_TRACKER[0]["status"] = f"System Halted: Engine Config Error"

# --- 4. API FORM ENTRY POINT ---
@app.post("/start-automation")
async def start_automation(
    background_tasks: BackgroundTasks,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    keywords: str = Form(...),
    location: str = Form(...),
    resume: UploadFile = File(...)
):
    global APPLIED_JOBS_TRACKER
    APPLIED_JOBS_TRACKER = []
    
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(resume_path, "wb") as buffer:
        buffer.write(await resume.read())
        
    user_info = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "resume_path": resume_path
    }
    
    background_tasks.add_task(run_job_automation, user_info, keywords, location)
    return RedirectResponse(url="/tracker", status_code=303)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
