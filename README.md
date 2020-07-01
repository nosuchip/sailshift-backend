# Sailshift backend

## Deployment explanation

Application currently served from Elastic Beanstalk on AWS infrastructure. All settign are defined through environment
variables and only affects the backend. Frontend must be provided by settings devined in env,vars by API response
and it should be avoided to have build-time variables (usually prefiexed by `VUE_APP_*`).

Frontend server as fallback url handler by backend i.e. when no other routes handles URL it will be passed to
frontend package router.

On EBS static assets serverd by Nginx proxy (see `nginx.conf`).

## Development procedure

Application consist of 2 parts - backend and frontend.

Backend is Python3-powered application that uses Flask for API server implementation and MySQL as database. For database
access uses SQLAlchemy (everything latest version at the moment of development - 2020-07-01).

Frontend is progressive SPA implemented using Vue.js and Typescript and must be compiled before deployment.

To make everything simpler both apps should be places on predefined directories to maintain development process
described below.

### Prerequisites
Install globally AWS EB CLI tool: `pip3 install awsebcli`. Sometimes `pip3` unavailable and then check before
that Python3 is installed: `python --version`. If it shown something like `3.x` then check what Python used by `pip`:
`pip --version`. It shows something like `pip 20.1.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)` -
it uses python 3.x so it is ok. If Python2.x shown then Python3 *must* be installed as app is incompatible with
Python2.

Expected that appropriate EBS environment created, EB credentials are set and it is ready to work. Further instructions
will not cover this process.

### App building

- both apps cloned to appropriate directories under same parent directory:
    - backend code placed in `backend` directory
    - frontend code placed in `frontend` directory
- navigate to frontend directory
    - install dependencies: `npm install`
    - build production bundle: `npm run build`
    - NOTE: developer must check first that changes implemented are correct and application able to run correct
        and buildable (it is not the same)
- navigate to backed directory
    - update static assets and rewrite some paths: `./update_static.sh`
    - add new files to git: `git add . && git commit -a -m "Update UI"`
    - push change to Git repo: `git push`
    - check everything locally and theh merge changes to git `production` branch:
        `git checkout production && git merge master`

### App deploying

- navigate to backed directory
- deploy change to EBS: `eb deploy`
- open EBS dashboard and ensure that its `health` mark is green.
- open `https://sailshift.com` and ensure that changes are reflected there

As an option developer can zip ready application folder and upload it viue EBS dashboard. Indeed this isn't recommended
way to deploy applicaiton.

### App settings change

- open EBS dashboard
- click "Configuation"
- click "Edit" on "Software" panel
- scroll down to section "Environment"
- update required variables and click "Apply"

Application restart and new change will be applied to newly started app.
