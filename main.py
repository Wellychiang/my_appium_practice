import pytest
import sys
import os

if __name__ == '__main__':
    # pytest.main(['-vvs', '--reruns', '1', '--alluredir', 'report'])
    os.system('rmdir /s /q allure-report')
    os.system('rmdir /s /q report')

    if str(sys.argv[1]) == 'features' or str(sys.argv[1]) == 'stories':
        pytest.main([
            '-vvs',
            '--reruns', '1',
            f'--allure-{str(sys.argv[1])}',
            str(sys.argv[2]),
            '--alluredir', 'report'
        ])
        print(sys.argv[1], sys.argv[2])
    elif str(sys.argv[1]) == 'all':
        pytest.main(['-vvs', '--alluredir', 'report'])
        print(sys.argv[1])

    else:
        raise ValueError("You can only input 'all, features or stories' in argv[1]")


