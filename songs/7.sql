SELECT avg(energy) as AverageEnergyDrake FROM songs
WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake")
