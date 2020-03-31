# Cloudlet development methodology
This page explains the way that we will work in the connected environment, from the point the developer starts working on a new feature to the point that he declares that his work is finished. 
## Making your personal branch
Every developer will create his personal branch:
``` 
git checkout -b <your_name>
```
In this branch the developer will write his own code without any limits.
## Creating a pull request
When the developer thinks that his new feature is ready for production, he creates a pull request to branch release-2.x(our release number). At least two team members will go over his feature and they will check the quality of his code (if he adds a code to the feature), check the documentation and if it can be transfered to the disconnected environment.
##  Note
Remember when you are doing git pull write the branch that you work with:
```
git pull origin <your_branch>
```
