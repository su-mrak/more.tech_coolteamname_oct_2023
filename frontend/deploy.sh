#!/bin/bash

aws s3 --endpoint-url=https://storage.yandexcloud.net rm s3://more-tech-front --recursive
aws s3 --endpoint-url=https://storage.yandexcloud.net sync ./dist s3://more-tech-front
