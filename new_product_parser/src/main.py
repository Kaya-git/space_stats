from rbtmq_handler import rbtmq
import sys
import os


async def main()
    rbtmq.consume()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
