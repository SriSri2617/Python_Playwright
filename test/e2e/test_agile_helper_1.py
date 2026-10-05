import re
from playwright.sync_api import Page, expect

base_url = "https://lejonmanen.github.io/agile-helper/"

# User story 1 : As a user, I want to view the Agile Helper page, 
# so that I can access information about Agile and Scrum practices.

def test_agile_helper_homepage(page: Page):
    # page load
    page.goto(base_url)
    
    #Page title verification
    expect(page).to_have_title(re.compile("Agile helper"))
    
    #Flags img verification
    # Swedish flag
    sv_flag = page.get_by_test_id("language-sv")
    # British flag
    en_flag = page.get_by_test_id("language-en")  
      
    expect(sv_flag).to_be_visible()
    expect(en_flag).to_be_visible()
    
    #Heading verification
    day_heading = page.locator("p", has_text=re.compile("Vilken dag under sprinten är det?"))
    expect(day_heading).to_be_visible()
    
    #Button verification(Första, mitt, Sista)
    btn_first = page.get_by_test_id("btn-first")
    btn_middle = page.get_by_test_id("btn-middle")
    btn_last = page.get_by_test_id("btn-last")
    
    expect(btn_first).to_be_visible()     
    expect(btn_middle).to_be_visible()    
    expect(btn_last).to_be_visible()
    
    #page interaction verification
    btn_first.click()

    first_day_heading = page.locator("p", has_text=re.compile("Första dagen i sprinten."))
    expect(first_day_heading).to_be_visible()
    
#-----------------------------------------------------------------------------------

# User story 2 : As a user, I want to view the Agile Helper page in English, 
# so that I can understand the information even if I do not speak Swedish.

def test_Lang_flag(page: Page):
    # page load
    page.goto(base_url)
    
    #En flag verification
    en_flag = page.get_by_test_id("language-en")  
    en_flag.click()
    
    # Heading verification
    day_heading = page.locator("p", has_text="What day of the sprint is it?")
    expect(day_heading).to_be_visible()
    
    # buttons in en - verification
    expect(page.get_by_role("button").get_by_text(re.compile("First"))).to_be_visible()
    expect(page.get_by_role("button").get_by_text(re.compile("Somewhere in the middle"))).to_be_visible()
    expect(page.get_by_role("button").get_by_text(re.compile("Last"))).to_be_visible()
    
    # page load verification
    page.get_by_role("button", name=re.compile("Somewhere in the middle")).click()
    expect(page.get_by_text(re.compile("Any day during the sprint."))).to_be_visible()
    expect(page.get_by_text(re.compile("Sprint planning"))).to_be_visible()
    
#-----------------------------------------------------------------------------------

# User story 3 : As a user, I want to see instructions for Sprint Planning on the first day of the sprint, 
# so that I know how to prepare the sprint backlog. 

def test_sprint_first_day_page(page: Page):
    # page load
    page.goto(base_url)
    
    #language en 
    page.get_by_test_id("language-en").click()
    
    # button first
    page.get_by_test_id("btn-first").click()
    
    #page verification
    expect(page.get_by_text(re.compile("First day of sprint."))).to_be_visible()
    
    # buttons verification
    expect(page.get_by_test_id("btn-restart")).to_be_visible()
    expect(page.get_by_role("button")
           .get_by_text(re.compile("Start off the sprint with Sprint planning"))).to_be_visible()
    expect(page.get_by_role("button")
           .get_by_text(re.compile("Start every day with Daily standup"))).to_be_visible()
    
    # Sprint planning button
    page.get_by_role("button", name=re.compile("Start off the sprint with Sprint planning")).click()
    sprint_plan_info = page.get_by_role("heading", name=re.compile("Sprint planning"))
    expect(sprint_plan_info).to_be_visible()
        
    # Ok we're done button    
    page.get_by_role("button", name="Ok we're done. Start the sprint!").click()
    sprint_plan_dialog = page.locator(".sprint-ceremony dialog show")
    expect(sprint_plan_dialog).not_to_be_visible()
      

#-----------------------------------------------------------------------------------

# User Story 4 : As a user, I want to see instructions for Daily Standup, 
# so that I know what to discuss during the daily meeting.

def test_sprint_first_day_daily_standup(page: Page):
    # page load
    page.goto(base_url)

    # language en 
    page.get_by_test_id("language-en").click()

    # button first
    page.get_by_test_id("btn-first").click()

    # Daily standup button
    page.get_by_role("button", name="Start every day with Daily standup").click()
    daily_standup_info = page.get_by_role("heading", name = "Daily standup")
    expect(daily_standup_info).to_be_visible()
    
    # Start the meeting button
    page.get_by_role("button", name="Start the meeting: 10 minutes").click()

    # time left box
    expect(page.get_by_text("Time left:")).to_be_visible()
    timer = page.locator("span.framed")
    before_timer = timer.text_content()
    page.wait_for_timeout(2000)
    after_timer = timer.text_content()
    assert before_timer != after_timer

    # Ok we're done button    
    page.get_by_role("button", name="Ok we're done!").click()
    sprint_plan_dialog = page.locator(".sprint-ceremony dialog show")
    expect(sprint_plan_dialog).not_to_be_visible()
   
#-----------------------------------------------------------------------------------
    

    

