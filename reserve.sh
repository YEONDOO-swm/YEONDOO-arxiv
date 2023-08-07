#!/bin/bash

# 3시간을 초로 환산한 값을 계산합니다.
seconds_to_wait=$((10800))

# 3시간 동안 대기합니다.
sleep $seconds_to_wait

# test.py를 실행합니다.
#python3 test.py
python3 wrapper.py 2>&1 | tee -a final_output.log
