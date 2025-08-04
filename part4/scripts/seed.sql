-- Insert Admin User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$4mJZTFslW7RT4lZRLcYXsOnhHVcf.OJcqNAgId5ltLyd0uS86ZUlK', -- bcrypt hash of "admin1234"
    TRUE
);

-- Insert Amenities
INSERT INTO amenities (id, name)
VALUES
    ('9ba6b7aa-3731-4223-92ee-f56de70846f3', 'WiFi'),
    ('dd5b1267-1e0d-49d4-88fd-54ac8d32a2ba', 'Swimming Pool'),
    ('a2ff8c7a-4ffa-4ef5-92dd-0866121233a1', 'Air Conditioning');
