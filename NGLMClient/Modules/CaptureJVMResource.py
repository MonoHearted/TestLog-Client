import logging
import os
import subprocess
import sys
import time
import re

logger = logging.getLogger(__name__)


class CaptureJVMResource(object):

    def __init__(self, javaHome, interval, pid):
        self._javaHome = javaHome
        self._interval = interval
        self._pid = pid
        self._jvmTop = os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            "Tools",
            "jvmtop.sh"
        )
        if (not os.path.exists(self._jvmTop)):
            raise Exception("Jvmtop doesn't exist")

    # async runTask(itr):

    def startJob(self, itr):
        timeout = self._interval * (itr + 1)
        os.environ['JAVA_HOME'] = self._javaHome
        # check java home
        try:
            if (not subprocess.check_call([os.path.join(self._javaHome, 'bin',
                                                        "java"),
                                           "-version"])):
                pass
        except ChildProcessError or FileNotFoundError as cpe:
            logger.error("JAVA_HOME is incorrect")
            raise cpe

        try:
            sp = subprocess.Popen(['bash', self._jvmTop, str(self._pid),
                                   '-d', str(self._interval),
                                   '-n', str(itr)],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        except Exception as e:
            logger.debug(e)
            raise e

        startTime = time.time()
        HeapPattern = re.compile(
            r'\s+CPU:.*GC:\s+([0-9]+\.[0-9][0-9])%\s+'
            r'HEAP:\s*(\d+)m\s+\/\d+m NONHEAP:\s*(\d*)m?\s+\/\d+m.*$'
        )
        try:
            logger.info("Start Jvmtop @ %d" % startTime)
            output = sp.stdout.readline().decode('ascii').rstrip()
            while (time.time() - startTime < timeout):
                if "exception" in output.lower():
                        # or "error" in output.lower():
                    raise Exception("JVMTop Failed: %s" % output)
                # logger.debug(output)
                HeapMatched = HeapPattern.match(output)
                if (HeapMatched is not None):
                    try:
                        int(HeapMatched.group(3))
                    except ValueError:
                        retDict = {
                            "GC FREE PERCENTAGE": float(HeapMatched.group(1)),
                            "HEAP SIZE IN BYTES": int(HeapMatched.group(2))
                        }
                    else:
                        retDict = {
                            "GC FREE PERCENTAGE": float(HeapMatched.group(1)),
                            "HEAP SIZE IN BYTES": int(HeapMatched.group(2)),
                            "NONHEAP SIZE IN BYTES": int(HeapMatched.group(3))
                        }
                    logger.debug(retDict)
                    yield retDict
                output = sp.stdout.readline().decode('ascii').rstrip()

        except ChildProcessError:
            sp.kill()
            output, err = sp.communicate()
            output = output.decode('ascii').rstrip()
            err = err.decode('ascii').rstrip()
            logger.error("Exception: %s\n%s" % (output, err))
        # in case child process hang there after timeout
        # wait for 30 more seconds and exit
        try:
            sp.wait(30)
        except:
            logger.warning('The subprocess was forced to exit after waiting '
                           'for 30 seconds.')
