import re
from playwright.sync_api import Page, expect

base_url = "https://lejonmanen.github.io/agile-helper/"

# User Story 5 : As a user, I want to choose another day in the sprint, 
# so that I can view the activities and meetings that take place on different days of the sprint.

def test_sprint_first_day_page(page: Page):
    # page load
    page.goto(base_url)

    # language en 
    page.get_by_test_id("language-en").click()

    # button first
    page.get_by_test_id("btn-first").click()
    
    # button name change after first day selected
    btn_restart = page.get_by_test_id("btn-restart")
    btn_restart.click()
    
    # sprint day selection button
    btn_first = page.get_by_test_id("btn-first")
    btn_middle = page.get_by_test_id("btn-middle")
    btn_last = page.get_by_test_id("btn-last")

    expect(btn_first).to_be_visible()
    expect(btn_middle).to_be_visible()
    expect(btn_last).to_be_visible()
    
    # select somewhere in the middle
    btn_middle.click()
    expect(page.get_by_text(re.compile("Any day during the sprint."))).to_be_visible()
    
    # select last day
    btn_restart.click()
    btn_last.click()
    expect(page.get_by_text(re.compile("Final day of the sprint."))).to_be_visible()
    
#-----------------------------------------------------------------------------------
    
#User Story 6 : As a user, I want to see information about Sprint Review at the end of the sprint, 
#so that I know how to demonstrate completed work to stakeholders. 

# User Story 7 : As a user, I want to see instructions for Sprint Retrospective, 
# so that my team can evaluate the sprint and identify improvements for future sprints.

def test_sprint_last_day_page(page: Page):
    # page load
    page.goto(base_url)

    # language en 
    page.get_by_test_id("language-en").click()

    # button last
    btn_last = page.get_by_test_id("btn-last")
    btn_last.click()
    expect(page.get_by_text(re.compile("Final day of the sprint."))).to_be_visible()
    
    # button verification
    btn_daily_standup = page.get_by_role("button", name = re.compile("Daily standup"))
    expect(btn_daily_standup).to_be_visible()

    btn_sprint_review = page.get_by_role("button", name=re.compile("Sprint review"))
    expect(btn_sprint_review).to_be_visible()

    btn_sprint_retro = page.get_by_role("button", name=re.compile("Sprint retrospective"))
    expect(btn_sprint_retro).to_be_visible()
    
    # sprint review info verification
    btn_sprint_review.click()
    
    expect(page.get_by_role("heading", name = re.compile("Sprint review"))).to_be_visible()

    # Ok we're done. Onwards to retrospective! button
    btn_onwards_to_retro = page.get_by_role("button", name=re.compile("Onwards to retrospective!"))
    btn_onwards_to_retro.click()

    sprint_plan_dialog = page.locator(".sprint-ceremony dialog show")
    expect(sprint_plan_dialog).not_to_be_visible()
    
    # End the sprint by evaluating your work in Sprint retrospective button
    btn_sprint_retro.click()
    expect(page.get_by_role("heading", name=re.compile("Sprint retrospective"))).to_be_visible()
    
    #The sprint is complete button
    btn_sprint_complete = page.get_by_role("button", name = re.compile("sprint is complete"))
    btn_sprint_complete.click()
    
    sprint_plan_dialog = page.locator(".sprint-ceremony dialog show")
    expect(sprint_plan_dialog).not_to_be_visible()

    # after closing the session, verify that it's in the same " Final day of sprint" page
    expect(page.get_by_text(re.compile("Final day of the sprint."))).to_be_visible()

#-----------------------------------------------------------------------------------
