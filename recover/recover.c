#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

#define BLOCK_SIZE 512
#define FILENAME_SIZE 8

int main(int argc, char *argv[])
{
    // Check for correct number of command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open input file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    int jpg_count = 0;
    FILE *img = NULL;
    char filename[FILENAME_SIZE];

    while (fread(buffer, BLOCK_SIZE, 1, file) == 1)
    {
        // Check for start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous image file if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", jpg_count++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(file);
                fprintf(stderr, "Could not create output file.\n");
                return 2;
            }
        }

        // Write to the JPEG file
        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    // Close input file
    fclose(file);

    return 0;
}
