
def failed_login(username, pwd, err_msg, login_page):

    login_page.input_username(account=username)
    login_page.input_pwd(pwd=pwd)
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.close_keyboard()
    login_page.check_error_msg(err_msg=err_msg)


