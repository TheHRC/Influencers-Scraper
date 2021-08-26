import os


def get_insta_cred():
    """
        Sets Instagram credentials if not found
        and returns
    :return (str, str)
    """
    if "i_u_name" in os.environ and "i_u_pass" in os.environ:

        user_name = os.getenv('i_u_name')
        user_pass = os.environ.get('i_u_pass')
    else:
        user_name = input("Enter your Instagram UserId: ").strip()
        user_pass = input("Enter your Instagram Password: ").strip()

        os.environ["i_u_name"] = user_name
        os.environ["i_u_pass"] = user_pass

    return (user_name,user_pass)

def get_hydeauditor_cred():
    """
           Sets Hypeauditor credentials if not found
           and returns
       :return (str, str)
       """
    if "hypeauditor_name" in os.environ and "hypeauditor_pass" in os.environ:

        h_name = os.getenv('hypeauditor_name')
        h_pass = os.environ.get('hypeauditor_pass')
    else:
        h_name = input("Enter your Hypeauditor UserId: ").strip()
        h_pass = input("Enter your Hypeauditor Password: ").strip()

        os.environ["hypeauditor_name"] = h_name
        os.environ["hypeauditor_pass"] = h_pass
    return (h_name, h_pass)
