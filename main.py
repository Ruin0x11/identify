import analyze
import pandas as pd
import sys
import matplotlib.pyplot as plt


def main():
    name = sys.argv[1]
    result = analyze.analyze(name)
    with pd.option_context('display.max_rows', None):
        print(result.to_csv())
    result.plot(x='min', y='max', style='o')
    plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
