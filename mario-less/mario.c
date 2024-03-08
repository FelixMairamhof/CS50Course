#include <cs50.h>
#include <stdio.h>

void drawPyramid(void);

int main(void)
{
    drawPyramid();
}
void drawPyramid(void)
{
    int size;
    do
    {
        size = get_int("Height: ");
    }
    while (size < 1 || size > 8);

    // printf("Stored: %d",size);

    for (int i = 1; i <= size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            if (j < size - i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
