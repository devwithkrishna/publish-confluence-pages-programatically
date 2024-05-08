import argparse
import os
import markdown
from atlassian import Confluence
from dotenv import load_dotenv


def confluence_client(confluence_url: str, username: str, password: str):
    """
    Create confluence client for authentication
    :return:
    """

    confluence_client = Confluence(
        url=confluence_url,
        username=username,
        password=password,
        cloud=True)
    return confluence_client


def get_confluence_page_id(confluence_client, confluence_space: str, confluence_page_title: str):
    """
    return confluence page id
    :return:
    """
    confluence = confluence_client
    confluence_page_id = confluence.get_page_id(space=confluence_space,
                                                title=confluence_page_title)
    return confluence_page_id


def render_html_from_md_file(markdown_file_path: str):
    """
    Render html content to pass to confluence object from markdown file
    :param markdown_file_path:
    :return:
    """
    markdown_file_path = markdown_file_path
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)
    return html_content


def create_confluence_page(confluence_client, html_content, confluence_space: str, confluence_page_title: str):
    """
    Create a confluence page using python sdk
    :return:
    """
    confluence = confluence_client

    status = confluence.create_page(
        space=confluence_space,
        title=confluence_page_title,
        body=html_content
    )

    print(status)


def update_confluence_page_if_exists(confluence_client, html_content, confluence_page_id: str, confluence_page_title: str):
    """
    update an existing confluence page - clear and write fresh if existing
    :param confluence_client:
    :param html_content:
    :param confluence_page_id:
    :param confluence_page_title:
    :return:
    """
    confluence = confluence_client
    status = confluence.update_page(
        page_id=confluence_page_id,
        title=confluence_page_title,
        body=html_content
    )
    print(status)


def append_body_to_page(confluence_client, html_content, confluence_page_id: str, confluence_page_title:str):
    """
    Append body to page if already exist
    :return:
    """
    confluence = confluence_client
    status = confluence.append_page(
        page_id=confluence_page_id,
        title=confluence_page_title,
        append_body=html_content
    )
    print(status)

def main():
    """ To test the script"""
    parser = argparse.ArgumentParser(description='Process arguments for the program')
    parser.add_argument("--confluence_space", type=str, help='Confluencce space', required=True)
    parser.add_argument("--confluence_page_title", type=str, help='Confluence page title', required=True)
    parser.add_argument("--markdown_file_path", type=str, help='Markdown file path with file name', required=True)

    load_dotenv()
    confluence_url = os.getenv('CONFLUENCE_URL')
    print(confluence_url)
    usernname = os.getenv('CONFLUENCE_USERNAME')
    print(usernname)
    password = os.getenv('CONFLUENCE_PASSWORD')
    print(password)

    args = parser.parse_args()
    confluence_space = args.confluence_space
    confluence_page_title = args.confluence_page_title
    markdown_file_path = args.markdown_file_path

    # function call
    confluence = confluence_client(confluence_url=confluence_url, username=usernname, password=password)
    html_content = render_html_from_md_file(markdown_file_path=markdown_file_path)
    # create_confluence_page(confluence_client=confluence, html_content=html_content)
    confluence_page_id = get_confluence_page_id(confluence_client=confluence, confluence_space=confluence_space,
                                                confluence_page_title=confluence_page_title)
    # update_confluence_page_if_exists(confluence_client=confluence, confluence_page_id=confluence_page_id,
    #                        html_content=html_content,confluence_page_title=confluence_page_title)
    # append_body_to_page(confluence_client=confluence,confluence_page_title=confluence_page_title,
    #                     confluence_page_id=confluence_page_id,html_content=html_content)

if __name__ == "__main__":
    main()
