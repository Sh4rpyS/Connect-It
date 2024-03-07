import game

def main() -> None:
    game.Init(2500, False)
    game.Start_Game()

if __name__ == "__main__":
    # Change between True and False to switch the profiler on/off
    if False:
        import cProfile
        cProfile.run('main()', "profiler/output.dat")

        import pstats
        from pstats import SortKey

        with open("profiler/output_time.txt", "w") as f:
            p = pstats.Stats("profiler/output.dat", stream=f)
            p.sort_stats("time").print_stats()

        with open("profiler/output_calls.txt", "w") as f:
            p = pstats.Stats("profiler/output.dat", stream=f)
            p.sort_stats("calls").print_stats()
    else:
        main()