# placeholder so the docker workflow has something to build - the real image
# (python base, requirements, flask on 0.0.0.0) comes in its own issue, see docs/deployment/docker.md
FROM alpine:3.20
CMD ["echo", "placeholder image - the app is not packaged yet"]
