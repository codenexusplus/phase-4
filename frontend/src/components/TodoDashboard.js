import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import axios from 'axios';
import API_BASE_URL from '../api';
import { useAuth } from '../contexts/AuthContext';

const TodoDashboard = forwardRef(({ onRefresh }, ref) => {
  const { token, user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Expose fetchTasks function to parent component
  useImperativeHandle(ref, () => ({
    fetchTasks
  }));

  // Fetch tasks when component mounts or when tasks change
  useEffect(() => {
    fetchTasks();
  }, [user, token]);

  // State for editing tasks - moved to top to comply with React Hooks rules
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');
  const [editingTaskDescription, setEditingTaskDescription] = useState('');

  const fetchTasks = async () => {
    if (!user || !token) return;

    try {
      setLoading(true);
      // Using user.id as the user identifier in the API endpoint
      const response = await axios.get(`${API_BASE_URL}/api/${user.id}/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTasks(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to fetch tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e) => {
    e.preventDefault();

    if (!newTaskTitle.trim() || !user || !token) return;

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/${user.id}/tasks`,
        {
          title: newTaskTitle,
          description: '',  // Send empty description as it's optional
          completed: false  // Explicitly set completed to false
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setTasks([...tasks, response.data]);
      setNewTaskTitle('');
      if (onRefresh) onRefresh(); // Call the refresh function if provided
    } catch (err) {
      console.error('Error adding task:', err);
      console.error('Error response:', err.response); // Log the full error response
      setError('Failed to add task. Please try again.');
    }
  };

  const toggleTaskCompletion = async (taskId, currentStatus) => {
    if (!user || !token) return;

    try {
      const response = await axios.patch(
        `${API_BASE_URL}/api/${user.id}/tasks/${taskId}/complete`,
        { completed: !currentStatus },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed: !currentStatus } : task
      ));
      if (onRefresh) onRefresh(); // Call the refresh function if provided
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  const deleteTask = async (taskId) => {
    if (!user || !token) return;

    try {
      await axios.delete(
        `${API_BASE_URL}/api/${user.id}/tasks/${taskId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setTasks(tasks.filter(task => task.id !== taskId));
      if (onRefresh) onRefresh(); // Call the refresh function if provided
    } catch (err) {
      console.error('Error deleting task:', err);
      setError('Failed to delete task. Please try again.');
    }
  };

  // Function to start editing a task
  const startEditing = (task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
    setEditingTaskDescription(task.description || '');
  };

  // Function to save edited task
  const saveEditedTask = async (taskId) => {
    if (!user || !token) return;

    try {
      const response = await axios.put(
        `${API_BASE_URL}/api/${user.id}/tasks/${taskId}`,
        {
          title: editingTaskTitle,
          description: editingTaskDescription,
          completed: tasks.find(t => t.id === taskId)?.completed || false
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? response.data : task
      ));

      // Exit edit mode
      setEditingTaskId(null);
      if (onRefresh) onRefresh(); // Call the refresh function if provided
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading tasks...</div>;
  }

  return (
    <div className="todo-dashboard">
      <h2>Your Tasks</h2>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={addTask} className="add-task-form">
        <input
          type="text"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          placeholder="Enter a new task..."
          className="task-input"
        />
        <button type="submit" className="add-task-button">Add Task</button>
      </form>

      <div className="tasks-list">
        {tasks.length === 0 ? (
          <p className="no-tasks">No tasks yet. Add a task to get started!</p>
        ) : (
          <ul>
            {tasks.map(task => (
              <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                {editingTaskId === task.id ? (
                  // Edit mode
                  <div className="task-edit-form">
                    <input
                      type="text"
                      value={editingTaskTitle}
                      onChange={(e) => setEditingTaskTitle(e.target.value)}
                      className="edit-task-title"
                      placeholder="Task title"
                    />
                    <textarea
                      value={editingTaskDescription}
                      onChange={(e) => setEditingTaskDescription(e.target.value)}
                      className="edit-task-description"
                      placeholder="Task description (optional)"
                    />
                    <div className="edit-actions">
                      <button
                        onClick={() => saveEditedTask(task.id)}
                        className="save-task-button"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingTaskId(null)}
                        className="cancel-edit-button"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  // Display mode
                  <>
                    <div className="task-content">
                      <h3 className="task-title">{task.title}</h3>
                      {task.description && (
                        <p className="task-description">{task.description}</p>
                      )}
                    </div>
                    <div className="task-actions">
                      <button
                        onClick={() => toggleTaskCompletion(task.id, task.completed)}
                        className={`toggle-complete ${task.completed ? 'completed-btn' : 'incomplete-btn'}`}
                      >
                        {task.completed ? 'Undo' : 'Complete'}
                      </button>
                      <button
                        onClick={() => startEditing(task)}
                        className="edit-task"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="delete-task"
                      >
                        Delete
                      </button>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
});

export default TodoDashboard;