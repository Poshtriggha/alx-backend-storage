-- Create function SafeDiv
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 4)
BEGIN
    DECLARE result DECIMAL(10, 4);
    
    IF b = 0 THEN
        RETURN 0;
    ELSE
        SET result = a / b;
        RETURN result;
    END IF;
END //

DELIMITER ;
