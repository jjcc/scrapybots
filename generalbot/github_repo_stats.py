from github import Github
from operator import itemgetter
from datetime import datetime
from dateutil.relativedelta import relativedelta

GITHUB_USERNAME = ''
GITHUB_PASSWORD = ''


def main(user, github_client=Github(GITHUB_USERNAME, GITHUB_PASSWORD)):
    """

    :param user: GitHub username.
    :param github_client: Optional. A github.MainClass.Github object.
        Should include a GitHub username and password for authentication.

    """

    # Get the 3 most popular repos
    popular_repos = get_popular_repos(github_client, user)

    # Get key statistics for repos
    data = []
    for r in popular_repos:
        data.append({'repo': r.name,'stats': get_repo_stats(r)})

    # Return result tied to user
    return {'user': user, 'data': data}


def get_popular_repos(github_client, user, top_n=3):
    """ Returns list of the top n most popular repos for a user.
    
    :param user: GitHub username.
    :param top_n: Default 3. Length of list to be returned.

    """

    popular_repos = []
    
    for r in github_client.get_user(user).get_repos():
        popularity_sum = r.stargazers_count + r.forks_count
        t = (popularity_sum, r)

        if len(popular_repos) < top_n:
            popular_repos.append(t)
            # Re-sort list by popularity sum
            popular_repos = sorted(popular_repos, 
                    key=itemgetter(0), reverse=True
                )

        elif popularity_sum > popular_repos[-1][0]:
            del popular_repos[-1]
            popular_repos.append(t)
            # Re-sort list by popularity sum
            popular_repos = sorted(popular_repos, 
                    key=itemgetter(0), reverse=True
                )

    return [repo[1] for repo in popular_repos]

def get_repo_stats(repo, last_n_months=6, repo_field_list=[
            'stargazers_count', 'forks_count', 'created_at', 'updated_at'
        ]):
    """ Returns key statistics for a repository.

    :param repo: github.Repository.Repository object.
    :param last_n_months: Default 6. Determines how many months of commits
        to request.
    :param repo_field_list: Optional. Modify if you want to get different 
        fields.

    """

    result = {}
    # Count up commits and unique contributors in last n months and store
    result['commits_last_{}_months'.format(last_n_months)], \
            result['contributors_last_{}_months'.format(last_n_months)] = \
            count_commits_and_contributors(repo)
    # Parse desired repo fields
    for f in repo_field_list:
        result[f] = getattr(repo, f)
    return result

def count_commits_and_contributors(repo, last_n_months=6):
    """ Returns the count of commits and unique contributors to a repository
    in a specified period of months.

    :param repo: github.Repository.Repository object.
    :param last_n_months: Default 6. Determines how many months of commits
        to request.

    """

    count_commits = 0
    count_contributors = 0
    contributors = []
    min_date = datetime.now() + relativedelta(months=-last_n_months)
    # Get commits from last n months
    commits = repo.get_commits(since=min_date)
    # Count up commits and unique contributors
    for c in commits:
        c = c.commit.committer
        count_commits += 1
        if c.name not in contributors:
            count_contributors+=1
            contributors.append(c.name)
    return count_commits, count_contributors


if __name__ == '__main__':
    # Sample for user "ripple"
    print (main('ripple'))

