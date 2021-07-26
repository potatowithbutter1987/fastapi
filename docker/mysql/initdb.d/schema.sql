CREATE TABLE vehicle_list (
    id INT NOT NULL AUTO_INCREMENT,
    maker_id INT NOT NULL COMMENT 'メーカID:',
    car_id INT NOT NULL COMMENT '車種ID',
    price INT NOT NULL COMMENT '価格',
    model_year VARCHAR(4) NOT NULL COMMENT '年式',
    mileage INT NOT NULL COMMENT '走行距離',
    unrunnable BOOLEAN COMMENT '自走可否',
    displacement INT NOT NULL COMMENT '排気量',
    vehicle_inspection_expiry INT NOT NULL COMMENT '車検残',
    car_name VARCHAR(255) NOT NULL COMMENT '車両名',
    area VARCHAR(255) NOT NULL COMMENT '地域',
    PRIMARY KEY (id)
);
ALTER TABLE vehicle_list ADD INDEX idx_vehicle(maker_id,car_id,price,model_year,mileage,unrunnable,displacement,vehicle_inspection_expiry);