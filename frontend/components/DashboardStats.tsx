'use client'

import { 
  DocumentTextIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'

const stats = [
  {
    name: 'Total Reports',
    value: '1,234',
    change: '+12%',
    changeType: 'positive',
    icon: DocumentTextIcon,
  },
  {
    name: 'Active Jobs',
    value: '23',
    change: '+5',
    changeType: 'positive',
    icon: ClockIcon,
  },
  {
    name: 'Completed Today',
    value: '45',
    change: '+8',
    changeType: 'positive',
    icon: CheckCircleIcon,
  },
  {
    name: 'Failed Jobs',
    value: '3',
    change: '-2',
    changeType: 'negative',
    icon: ExclamationTriangleIcon,
  },
]

export function DashboardStats() {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.name}
          className="card p-6 hover:shadow-md transition-shadow duration-200"
        >
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <item.icon
                className="h-8 w-8 text-gray-400 dark:text-gray-500"
                aria-hidden="true"
              />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                  {item.name}
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {item.value}
                  </div>
                  <div
                    className={`ml-2 flex items-baseline text-sm font-semibold ${
                      item.changeType === 'positive'
                        ? 'text-green-600 dark:text-green-400'
                        : 'text-red-600 dark:text-red-400'
                    }`}
                  >
                    {item.change}
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
