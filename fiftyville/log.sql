-- Keep a log of any SQL queries you execute as you solve the mystery.

--crime scene describtion
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
--at 10:15am; at bakery ;Vermüllung 16:36

--bakery at 9-17
SELECT b.*,p.*
FROM bakery_security_logs b
JOIN people p On b.license_plate = p.license_plate
WHERE b.year = 2023 AND b.month = 7 AND b.day = 28 AND b.hour >= 9 AND b.hour <= 17;

--Flight
SELECT f.id, f.origin_airport_id, f.destination_airport_id
FROM flights f
WHERE f.year = 2023 AND f.month = 7 AND f.day = 28;

--airports
SELECT *
FROM airports;

--people who flight
SELECT p.name, p.passport_number
FROM passengers pa
JOIN people p ON pa.passport_number = p.passport_number
WHERE pa.flight_id = (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 28);


--acomplice
SELECT DISTINCT p.name
FROM phone_calls pc
JOIN people p ON pc.caller = p.phone_number
WHERE pc.year = 2023 AND pc.month = 7 AND pc.day = 28
  AND p.passport_number <> 'ThiefPassportNumber';

