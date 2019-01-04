FROM williamyeh/ansible:centos7

ENV PLAYBOOK site.yml
ENV INVENTORY inventories/hosts

RUN ansible-playbook-wrapper
