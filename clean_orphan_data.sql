USE icourse;

-- 暂时禁用外键约束
SET FOREIGN_KEY_CHECKS=0;

-- 删除已删除用户相关的数据
DELETE FROM announcement WHERE author_id IN (1,2,3,5);
DELETE FROM announcement WHERE last_editor_id IN (1,2,3,5);
DELETE FROM course_info_history WHERE author IN (1,2,3,5);
DELETE FROM downvote_course WHERE user_id IN (1,2,3,5);
DELETE FROM follow_course WHERE user_id IN (1,2,3,5);
DELETE FROM follow_user WHERE follower_id IN (1,2,3,5);
DELETE FROM follow_user WHERE followed_id IN (1,2,3,5);
DELETE FROM forum_post_upvotes WHERE author_id IN (1,2,3,5);
DELETE FROM forum_posts WHERE author_id IN (1,2,3,5);
DELETE FROM forum_thread_upvotes WHERE author_id IN (1,2,3,5);
DELETE FROM forum_threads WHERE author_id IN (1,2,3,5);
DELETE FROM image_store WHERE author_id IN (1,2,3,5);
DELETE FROM note_comments WHERE author_id IN (1,2,3,5);
DELETE FROM note_upvotes WHERE author_id IN (1,2,3,5);
DELETE FROM notes WHERE author_id IN (1,2,3,5);
DELETE FROM notifications WHERE to_user_id IN (1,2,3,5);
DELETE FROM notifications WHERE from_user_id IN (1,2,3,5);
DELETE FROM review_comments WHERE author_id IN (1,2,3,5);
DELETE FROM review_course WHERE user_id IN (1,2,3,5);
DELETE FROM review_upvotes WHERE author_id IN (1,2,3,5);
DELETE FROM reviews WHERE author_id IN (1,2,3,5);
DELETE FROM search_log WHERE user_id IN (1,2,3,5);
DELETE FROM share_comments WHERE author_id IN (1,2,3,5);
DELETE FROM share_upvotes WHERE author_id IN (1,2,3,5);
DELETE FROM shares WHERE author_id IN (1,2,3,5);
DELETE FROM students WHERE user_id IN (1,2,3,5);
DELETE FROM teacher_info_history WHERE author IN (1,2,3,5);
DELETE FROM teachers WHERE user_id IN (1,2,3,5);
DELETE FROM upvote_course WHERE user_id IN (1,2,3,5);

-- 重新启用外键约束
SET FOREIGN_KEY_CHECKS=1; 