'use client'

import { useQuery } from '@tanstack/react-query'
import { researchJobsApi } from '@/lib/api/researchJobs'

export function ProgressChart() {
  const { data: stats } = useQuery({
    queryKey: ['research-jobs-stats'],
    queryFn: () => researchJobsApi.getStats(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  // Mock data for demonstration
  const chartData = [
    { date: '2024-01-01', completed: 5, active: 3, failed: 1 },
    { date: '2024-01-02', completed: 8, active: 2, failed: 1 },
    { date: '2024-01-03', completed: 12, active: 4, failed: 2 },
    { date: '2024-01-04', completed: 15, active: 3, failed: 2 },
    { date: '2024-01-05', completed: 18, active: 5, failed: 2 },
    { date: '2024-01-06', completed: 22, active: 4, failed: 3 },
    { date: '2024-01-07', completed: 25, active: 6, failed: 3 },
  ]

  return (
    <div className="space-y-4">
      {/* Chart Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Job Progress Over Time
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Last 7 days of research job activity
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600 dark:text-gray-400">Completed</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span className="text-sm text-gray-600 dark:text-gray-400">Active</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span className="text-sm text-gray-600 dark:text-gray-400">Failed</span>
          </div>
        </div>
      </div>

      {/* Chart Container */}
      <div className="relative h-64 bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
        <div className="flex items-end justify-between h-full space-x-2">
          {chartData.map((day, index) => (
            <div key={day.date} className="flex-1 flex flex-col items-center space-y-2">
              {/* Completed Jobs */}
              <div
                className="w-full bg-green-500 rounded-t"
                style={{
                  height: `${(day.completed / 25) * 100}%`,
                  minHeight: '4px',
                }}
              ></div>
              
              {/* Active Jobs */}
              <div
                className="w-full bg-blue-500 rounded-t"
                style={{
                  height: `${(day.active / 25) * 100}%`,
                  minHeight: '4px',
                }}
              ></div>
              
              {/* Failed Jobs */}
              <div
                className="w-full bg-red-500 rounded-t"
                style={{
                  height: `${(day.failed / 25) * 100}%`,
                  minHeight: '4px',
                }}
              ></div>
              
              {/* Date Label */}
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
            {stats?.stats?.completed_jobs || 25}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">Completed</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {stats?.stats?.active_jobs || 6}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">Active</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-red-600 dark:text-red-400">
            {stats?.stats?.failed_jobs || 3}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">Failed</div>
        </div>
      </div>
    </div>
  )
}
