'use client'

import { useQuery } from '@tanstack/react-query'
import { authApi } from '@/lib/api/auth'
import { ClockIcon, DocumentTextIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface ActivityFeedProps {
  limit?: number
}

export function ActivityFeed({ limit = 10 }: ActivityFeedProps) {
  const { data: activityData } = useQuery({
    queryKey: ['user-activity', limit],
    queryFn: () => authApi.getActivity({ limit }),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })

  // Mock data for demonstration
  const activities = [
    {
      id: '1',
      type: 'job_created',
      description: 'Created research job: Quantum Computing Trends',
      created_at: '2024-01-07T10:30:00Z',
      icon: DocumentTextIcon,
      color: 'text-blue-500',
    },
    {
      id: '2',
      type: 'job_completed',
      description: 'Completed research job: AI Ethics Analysis',
      created_at: '2024-01-07T09:15:00Z',
      icon: CheckCircleIcon,
      color: 'text-green-500',
    },
    {
      id: '3',
      type: 'report_downloaded',
      description: 'Downloaded report: Blockchain Technology Report',
      created_at: '2024-01-07T08:45:00Z',
      icon: DocumentTextIcon,
      color: 'text-purple-500',
    },
    {
      id: '4',
      type: 'job_failed',
      description: 'Research job failed: Climate Change Data',
      created_at: '2024-01-07T07:20:00Z',
      icon: ExclamationTriangleIcon,
      color: 'text-red-500',
    },
    {
      id: '5',
      type: 'job_started',
      description: 'Started research job: Renewable Energy Markets',
      created_at: '2024-01-07T06:30:00Z',
      icon: DocumentTextIcon,
      color: 'text-yellow-500',
    },
  ]

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'job_completed':
        return CheckCircleIcon
      case 'job_failed':
        return ExclamationTriangleIcon
      default:
        return DocumentTextIcon
    }
  }

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'job_completed':
        return 'text-green-500'
      case 'job_failed':
        return 'text-red-500'
      case 'job_started':
        return 'text-yellow-500'
      case 'report_downloaded':
        return 'text-purple-500'
      default:
        return 'text-blue-500'
    }
  }

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))

    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    return `${Math.floor(diffInMinutes / 1440)}d ago`
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          Recent Activity
        </h3>
        <button className="text-sm text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">
          View all
        </button>
      </div>

      <div className="flow-root">
        <ul className="-mb-8">
          {activities.slice(0, limit).map((activity, activityIdx) => {
            const ActivityIcon = getActivityIcon(activity.type)
            const activityColor = getActivityColor(activity.type)

            return (
              <li key={activity.id}>
                <div className="relative pb-8">
                  {activityIdx !== activities.length - 1 ? (
                    <span
                      className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200 dark:bg-gray-700"
                      aria-hidden="true"
                    />
                  ) : null}
                  <div className="relative flex space-x-3">
                    <div>
                      <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white dark:ring-gray-800 ${activityColor} bg-gray-50 dark:bg-gray-700`}>
                        <ActivityIcon className="h-5 w-5" aria-hidden="true" />
                      </span>
                    </div>
                    <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {activity.description}
                        </p>
                      </div>
                      <div className="whitespace-nowrap text-right text-sm text-gray-500 dark:text-gray-400">
                        <time dateTime={activity.created_at}>
                          {formatTimeAgo(activity.created_at)}
                        </time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            )
          })}
        </ul>
      </div>

      {activities.length === 0 && (
        <div className="text-center py-8">
          <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No recent activity
          </h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Start a research job to see activity here.
          </p>
        </div>
      )}
    </div>
  )
}
