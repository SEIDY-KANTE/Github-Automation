from github.github import Github

gitBot=Github()

#gitBot.signIn()

repositories=gitBot.getRepos()

print(f"{gitBot.getReposCount()} Repos exists\n")

for index, repo in enumerate(repositories):
    print(f"{'0' + str(index+1) if index+1 <10 else index+1 } : {repo}")
