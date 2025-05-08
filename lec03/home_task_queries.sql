/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT c.name         AS film_category,
       COUNT(film_id) AS num_films
FROM film f
         JOIN film_category fc USING (film_id)
         JOIN category c USING (category_id)
GROUP BY 1
ORDER BY 2 DESC;



/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/

-- The query to select exactly 10 actors with the highest number of the rented films.
-- This approach did not take into account that there can be several actors with the same number of films.
-- It simply takes 10 first records from the ordered query result using LIMIT.

SELECT a.first_name || ' ' || a.last_name AS actor,
       COUNT(rental_id)                   AS num_rentals
FROM rental r
         JOIN inventory i USING (inventory_id)
         JOIN film_actor fa USING (film_id)
         JOIN actor a USING (actor_id)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

--The alternative approach using ranking.
WITH actors_ranking AS
         (SELECT a.first_name || ' ' || a.last_name           AS actor,
                 COUNT(rental_id)                             AS num_rentals,
                 RANK() OVER (ORDER BY COUNT(rental_id) DESC) AS rank

          FROM rental r
                   JOIN inventory i USING (inventory_id)
                   JOIN film_actor fa USING (film_id)
                   JOIN actor a USING (actor_id)
          GROUP BY 1)

SELECT actor, num_rentals
FROM actors_ranking
WHERE rank <= 10;



/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT c.name      AS film_category,
       SUM(amount) AS rental_payments
FROM payment p
         JOIN rental r USING (rental_id)
         JOIN inventory i USING (inventory_id)
         JOIN film_category fc USING (film_id)
         JOIN category c USING (category_id)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT f.title AS films_not_in_inventory
FROM film f
         LEFT JOIN inventory i USING (film_id)
WHERE i.inventory_id IS NULL;


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/

-- The approach using ordering and LIMIT.
SELECT a.first_name || ' ' || a.last_name AS actor,
       COUNT(film_id) as num_children_films
FROM actor a
JOIN film_actor fa USING (actor_id)
JOIN film_category fc USING (film_id)
JOIN category c USING (category_id)
WHERE c.name = 'Children'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 3;

--The alternative approach using ranking.
WITH actors_ranking AS
         (SELECT a.first_name || ' ' || a.last_name         AS actor,
                 COUNT(film_id)                             AS num_children_films,
                 RANK() OVER (ORDER BY COUNT(film_id) DESC) AS rank
          FROM actor a
                   JOIN film_actor fa USING (actor_id)
                   JOIN film_category fc USING (film_id)
                   JOIN category c USING (category_id)
          WHERE c.name = 'Children'
          GROUP BY 1)

SELECT actor, num_children_films
FROM actors_ranking
WHERE rank <= 3;

