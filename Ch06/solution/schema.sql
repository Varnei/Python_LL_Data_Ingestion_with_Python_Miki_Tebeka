CREATE TABLE IF NOT EXISTS weather (
    day DATE,	    -- day of measurements
    min_temp FLOAT, -- min temperature in Fahrenheit
    max_temp FLOAT, -- max temperature in Fahrenheit
    snow INTEGETR   -- snow in inches
);

CREATE INDEX IF NOT EXISTS weather_day ON weather(day);
