#!/usr/bin/python3
import requests
import os
import sys

token = ''


def fetcher(username: str, selected_repo_num=15):
    result = {
        'name': '',
        'public_repos': 0,
        'selected_repos': []
    }
    user_info_url = "https://api.github.com/users/{}".format(username)
    all_repos_url = "https://api.github.com/users/{}/repos?per_page=100".format(username)
    header = {} if token == "" else {"Authorization": "bearer {}".format(token)}
    res = requests.get(user_info_url, header)
    user = res.json()
    result['name'] = user['name']
    res = requests.get(all_repos_url, header)
    repos = res.json()
    processed_repos = []
    for repo in repos:
        if repo['fork']:
            continue
        processed_repo = {
            'score': repo['stargazers_count'] + repo['watchers_count'] + repo['forks_count'],
            'star': repo['stargazers_count'],
            'link': repo['html_url'],
            'description': repo['description'],
            'last_update': repo['updated_at'],
        }
        processed_repos.append(processed_repo)
    selected_repos = sorted(processed_repos, key=lambda x: x['score'], reverse=True)
    selected_repos = selected_repos[:selected_repo_num]
    result['selected_repos'] = selected_repos
    return result


abstract_tpl = """## Abstract
![{github_username}'s Github Stats](https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&hide_border=true)
![{github_username}'s Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username={github_username}&layout=compact)
[![{zhihu_username}'s Zhihu Stats](https://stats.justsong.cn/api/zhihu?username={zhihu_username})](https://github.com/songquanpeng/readme-stats)
"""

selected_repos_tpl = """## Selected Repos
|Repo|Description|
|:--|:--|
|[{}]({})|{}|
"""


def render(github_data, zhihu_username='') -> str:
    markdown = ""
    print(github_data)
    return markdown


def main():
    if len(sys.argv) != 4:
        print("Error! This script requires one arguments: GITHUB_USERNAME GITHUB_TOKEN ZHIHU_USERNAME")
        return
    github_username = sys.argv[1]
    global token
    token = sys.argv[2]
    zhihu_username = sys.argv[1]
    github_data = fetcher(github_username)
    markdown = render(github_data, zhihu_username)
    print(markdown)


if __name__ == '__main__':
    main()