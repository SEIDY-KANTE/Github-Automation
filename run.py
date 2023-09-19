from github.github import Github
import json

gitBot=Github()

gitBot.signIn()

repositories=gitBot.getRepos()

print(f"{gitBot.getReposCount()} Repos exists\n")

for index, repo in enumerate(repositories):
    print(f"{'0' + str(index+1) if index+1 <10 else index+1 } : {repo}")


print("\n==================================================\n")

# print(f"You have : {gitBot.getFollowersCount()} Followers.")

followers=gitBot.getFollowers()
index=1
for follower in followers:
   
   print(f"User-{index}".center(50,'='))
   print(json.dumps(follower,indent=4))

   index+=1

#print(f"You have : {gitBot.getFollowersCount()} Followers.")