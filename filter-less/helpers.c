#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double red = image[i][j].rgbtRed;
            double green = image[i][j].rgbtGreen;
            double blue = image[i][j].rgbtBlue;

            int sum = round((red + green + blue) / 3.0);

            image[i][j].rgbtRed = sum;
            image[i][j].rgbtGreen = sum;
            image[i][j].rgbtBlue = sum;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double originalRed = image[i][j].rgbtRed;
            double originalGreen = image[i][j].rgbtGreen;
            double originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    // Iterate through each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redSum = 0, greenSum = 0, blueSum = 0;
            int count = 0;

            // Iterate through the surrounding pixels (3x3 box centered around the current pixel)
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int new_i = i + k;
                    int new_j = j + l;

                    // Check if the neighboring pixel is within bounds of the image
                    if (new_i >= 0 && new_i < height && new_j >= 0 && new_j < width)
                    {
                        // Accumulate the colors of the neighboring pixels
                        redSum += image[new_i][new_j].rgbtRed;
                        greenSum += image[new_i][new_j].rgbtGreen;
                        blueSum += image[new_i][new_j].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate the average color values for the current pixel
            temp[i][j].rgbtRed = (int) round((float) redSum / count);
            temp[i][j].rgbtGreen = (int) round((float) greenSum / count);
            temp[i][j].rgbtBlue = (int) round((float) blueSum / count);
        }
    }

    // Update the original image with the blurred version from the temporary image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}
