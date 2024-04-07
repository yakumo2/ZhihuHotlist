#!/bin/bash

echo "输入提交信息："
read message

git commit -m "$message"
git push -u origin main
