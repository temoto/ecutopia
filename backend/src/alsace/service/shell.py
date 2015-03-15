import IPython

import ecutopia.app


def main():
    app = ecutopia.app.init()
    with app.app_context():
        IPython.embed()

if __name__ == '__main__':
    main()
