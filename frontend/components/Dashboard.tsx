"""
Dashboard component for the Autonomous Research System.

This component provides a comprehensive overview of the user's research activities,
including statistics, recent jobs, charts, and real-time updates.
"""

import React, { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  ClockIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  PlusIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';
import { formatDistanceToNow, format } from 'date-fns';

import { api } from '../lib/api';
import { useAuth } from '../hooks/useAuth';
import { JobStatus, ResearchJob, JobStats } from '../types/research';
import DashboardStats from './DashboardStats';
import JobList from './JobList';
import JobCreationForm from './JobCreationForm';
import ProgressChart from './ProgressChart';
import ActivityFeed from './ActivityFeed';
import QuickActions from './QuickActions';

interface DashboardProps {
  className?: string;
}

const Dashboard: React.FC<DashboardProps> = ({ className = '' }) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedTimeRange, setSelectedTimeRange] = useState<'7d' | '30d' | '90d'>('30d');
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds

  // Fetch dashboard data
  const { data: stats, isLoading: statsLoading } = useQuery(
    ['dashboard-stats', selectedTimeRange],
    () => api.get(`/api/v1/research-jobs/stats/summary?time_range=${selectedTimeRange}`),
    {
      refetchInterval: refreshInterval,
      staleTime: 60000, // 1 minute
    }
  );

  // Fetch recent jobs
  const { data: recentJobs, isLoading: jobsLoading } = useQuery(
    ['recent-jobs'],
    () => api.get('/api/v1/research-jobs?page=1&size=5&sort_by=created_at&sort_order=desc'),
    {
      refetchInterval: refreshInterval,
      staleTime: 30000, // 30 seconds
    }
  );

  // Fetch activity feed
  const { data: activityFeed, isLoading: activityLoading } = useQuery(
    ['activity-feed'],
    () => api.get('/api/v1/users/activity?limit=10'),
    {
      refetchInterval: refreshInterval * 2, // 60 seconds
      staleTime: 120000, // 2 minutes
    }
  );

  // Create new research job
  const createJobMutation = useMutation(
    (jobData: any) => api.post('/api/v1/research-jobs', jobData),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['recent-jobs']);
        queryClient.invalidateQueries(['dashboard-stats']);
        setShowCreateForm(false);
        toast.success('Research job created successfully!');
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to create research job');
      },
    }
  );

  // Handle job actions
  const handleJobAction = useCallback(async (jobId: number, action: string) => {
    try {
      await api.post(`/api/v1/research-jobs/${jobId}/${action}`);
      queryClient.invalidateQueries(['recent-jobs']);
      queryClient.invalidateQueries(['dashboard-stats']);
      toast.success(`Job ${action}ed successfully!`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || `Failed to ${action} job`);
    }
  }, [queryClient]);

  // Auto-refresh based on active jobs
  useEffect(() => {
    const hasActiveJobs = recentJobs?.items?.some(
      (job: ResearchJob) => job.status === 'running' || job.status === 'processing'
    );
    
    if (hasActiveJobs) {
      setRefreshInterval(10000); // 10 seconds for active jobs
    } else {
      setRefreshInterval(30000); // 30 seconds for inactive jobs
    }
  }, [recentJobs]);

  const isLoading = statsLoading || jobsLoading || activityLoading;

  if (isLoading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-12 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Welcome back, {user?.first_name || user?.email}!
          </h1>
          <p className="text-gray-600 mt-1">
            Here's what's happening with your research projects
          </p>
        </div>
        <div className="flex items-center space-x-3 mt-4 sm:mt-0">
          <button
            onClick={() => setShowCreateForm(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Research
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <DashboardStats stats={stats?.data} />

      {/* Time Range Selector */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Research Overview</h2>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500">Time range:</span>
          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value as any)}
            className="text-sm border border-gray-300 rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Progress Chart */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Research Progress
            </h3>
            <ProgressChart 
              data={stats?.data} 
              timeRange={selectedTimeRange}
              className="h-64"
            />
          </div>
        </div>

        {/* Activity Feed */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Recent Activity
            </h3>
            <ActivityFeed 
              activities={activityFeed?.data?.items || []}
              className="space-y-3"
            />
          </div>
        </div>
      </div>

      {/* Recent Jobs */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              Recent Research Jobs
            </h3>
            <a
              href="/jobs"
              className="text-sm text-blue-600 hover:text-blue-500 font-medium"
            >
              View all →
            </a>
          </div>
          <JobList 
            jobs={recentJobs?.data?.items || []}
            onJobAction={handleJobAction}
            showPagination={false}
            className="space-y-3"
          />
        </div>
      </div>

      {/* Quick Actions */}
      <QuickActions 
        onCreateJob={() => setShowCreateForm(true)}
        className="bg-white rounded-lg shadow p-6"
      />

      {/* Create Job Modal */}
      <AnimatePresence>
        {showCreateForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={() => setShowCreateForm(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Create New Research Job
                  </h2>
                  <button
                    onClick={() => setShowCreateForm(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <span className="sr-only">Close</span>
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <JobCreationForm
                  onSubmit={createJobMutation.mutate}
                  isLoading={createJobMutation.isLoading}
                  onCancel={() => setShowCreateForm(false)}
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Dashboard;
