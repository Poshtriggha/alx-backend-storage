-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id_var INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;
    
    -- Declare cursor for selecting user IDs
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;
    
    -- Declare continue handler for cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open cursor
    OPEN user_cursor;
    
    -- Loop through all users
    user_loop: LOOP
        FETCH user_cursor INTO user_id_var;
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        -- Compute total weighted score for the current user
        SELECT SUM(score * weight) INTO total_score
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id_var;
        
        -- Compute total weight for the current user
        SELECT SUM(weight) INTO total_weight
        FROM projects;
        
        -- Compute average weighted score for the current user
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;
        
        -- Update average_score for the current user
        UPDATE users
        SET average_score = average_score
        WHERE id = user_id_var;
    END LOOP;
    
    -- Close cursor
    CLOSE user_cursor;
    
END //
DELIMITER ;
