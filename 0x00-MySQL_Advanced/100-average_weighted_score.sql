-- Create stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;

    -- Compute total weighted score
    SELECT SUM(score * weight) INTO total_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Compute total weight
    SELECT SUM(weight) INTO total_weight
    FROM projects;

    -- Compute average weighted score
    IF total_weight > 0 THEN
        SET average_score = total_score / total_weight;
    ELSE
        SET average_score = 0;
    END IF;

    -- Update average_score for the user
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //
DELIMITER ;
