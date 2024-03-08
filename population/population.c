#include <cs50.h>
#include <stdio.h>

int getStartSize(void);
int getEndSize(int start);
int getYears(int start, int end);

int main(void)
{
    // TODO: Prompt for start size
    int start = getStartSize();

    // TODO: Prompt for end size
    int end = getEndSize(start);
    // TODO: Calculate number of years until we reach threshold
    int years = getYears(start, end);
    // TODO: Print number of years
    printf("Years: %d\n", years);
}
int getStartSize(void)
{
    int startSize;
    do
    {
        startSize = get_int("Start size: ");
    }
    while (startSize < 9);
    return startSize;
}
int getEndSize(int start)
{
    int endSize;
    do
    {
        endSize = get_int("End size: ");
    }
    while (endSize < start);
    return endSize;
}
int getYears(int start, int end)
{
    int years = 0;
    while (start < end)
    {
        years++;
        start = start + (start / 3) - (start / 4);
    }
    return years;
}
