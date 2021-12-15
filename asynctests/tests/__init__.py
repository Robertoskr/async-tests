import asyncio
import concurrent.futures
import importlib
import os
import traceback
from datetime import datetime

N_THREADS = os.cpu_count()
DEFAULT_N_THREADS = 5


class Tester:
    def __init__(self):
        self.testfiles = []
        self.ntests = 0
        self.errors = []
        self.failures = []
        self.tests = []
        self.ntestsrun = 0
        self.counter = 0
        self.timetest = None
        self.work_queue = asyncio.Queue()

    def search_tests(self, path):
        resultfiles = []
        resultdirs = []
        for root, dirs, files in os.walk(path):
            if not root.startswith('_') and not root.startswith('.'):
                files = [
                    f'{root}.{file}'.replace('/', '.')
                    for file in files
                    if file.startswith('test') and file.find('pyc') == -1
                ]
                if len(files) > 0:
                    resultfiles.append(
                        file[file.find('src') : -3] for file in files  # noqa
                    )
                resultdirs.append(root)
        self.testfiles = resultfiles
        return resultfiles

    def getTests(self):
        tests = []
        for path in self.testfiles:
            for file in path:
                m = importlib.import_module(file)
                testclasses = [obj for obj in dir(m) if obj.startswith('Test')]
                for testclass in testclasses:
                    testmethods = [
                        method
                        for method in dir(getattr(m, testclass))
                        if method.startswith('test')
                    ]
                    for test in testmethods:
                        self.ntests += 1
                        tests.append((getattr(m, testclass)(), test))
        self.tests = tests
        return tests

    def runTest(self, testInfo):
        self.ntestsrun += 1
        try:
            testInfo[0].setUp()
            getattr(testInfo[0], testInfo[1])()
            testInfo[0].tearDown()
            print('.', end='')
        except AssertionError:
            self.failures.append(
                f'\n{testInfo[1].upper()} -> {traceback.format_exc()}'
            )
            print('F', end='')
        except Exception:
            self.errors.append(f'\n{testInfo[1]} -> {traceback.format_exc()}')
            print('E', end='')

    def runTests(self):
        async def _runTests():
            await asyncio.wait(
                fs=[
                    loop.run_in_executor(executor, self.runTest, testInfo)
                    for testInfo in self.tests
                ],
                return_when=asyncio.ALL_COMPLETED,
            )

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=(
                N_THREADS if N_THREADS is not None else DEFAULT_N_THREADS
            )
        )
        init = datetime.now()
        loop.run_until_complete(_runTests())
        end = datetime.now()
        self.timetest = end - init

    def run(self):
        self.search_tests(f'{os.getcwd()}/src')
        self.getTests()
        self.runTests()
        for failure in self.failures:
            print(failure)
        for error in self.errors:
            print(error)
        print(f'Run {self.ntestsrun} tests in {self.timetest}\n')


def run():
    tester = Tester()
    tester.run()