'use client'

import { useState } from 'react'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { 
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  EyeIcon,
  TrashIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { formatDistanceToNow } from 'date-fns'

// Mock data - replace with actual API calls
const mockJobs = [
  {
    id: '1',
    query: 'Impact of AI on healthcare delivery in the United States',
    status: 'completed',
    createdAt: new Date('2024-01-15T10:30:00Z'),
    completedAt: new Date('2024-01-15T14:45:00Z'),
    progress: 100,
    outputFormat: 'pdf',
  },
  {
    id: '2',
    query: 'Market analysis of renewable energy adoption in Europe',
    status: 'drafting',
    createdAt: new Date('2024-01-15T09:15:00Z'),
    progress: 65,
    outputFormat: 'docx',
  },
  {
    id: '3',
    query: 'Cybersecurity trends in financial services 2024',
    status: 'retrieving',
    createdAt: new Date('2024-01-15T08:00:00Z'),
    progress: 25,
    outputFormat: 'pptx',
  },
  {
    id: '4',
    query: 'Supply chain optimization strategies post-pandemic',
    status: 'failed',
    createdAt: new Date('2024-01-14T16:20:00Z'),
    progress: 0,
    outputFormat: 'pdf',
  },
]

const statusConfig = {
  pending: {
    label: 'Pending',
    icon: ClockIcon,
    className: 'status-pending',
  },
  planning: {
    label: 'Planning',
    icon: ClockIcon,
    className: 'status-planning',
  },
  retrieving: {
    label: 'Retrieving',
    icon: ArrowPathIcon,
    className: 'status-retrieving',
  },
  synthesizing: {
    label: 'Synthesizing',
    icon: ArrowPathIcon,
    className: 'status-synthesizing',
  },
  drafting: {
    label: 'Drafting',
    icon: DocumentTextIcon,
    className: 'status-drafting',
  },
  fact_checking: {
    label: 'Fact Checking',
    icon: ExclamationTriangleIcon,
    className: 'status-fact_checking',
  },
  visualizing: {
    label: 'Visualizing',
    icon: DocumentTextIcon,
    className: 'status-visualizing',
  },
  reviewing: {
    label: 'Reviewing',
    icon: ExclamationTriangleIcon,
    className: 'status-reviewing',
  },
  formatting: {
    label: 'Formatting',
    icon: DocumentTextIcon,
    className: 'status-formatting',
  },
  completed: {
    label: 'Completed',
    icon: CheckCircleIcon,
    className: 'status-completed',
  },
  failed: {
    label: 'Failed',
    icon: ExclamationTriangleIcon,
    className: 'status-failed',
  },
}

export function JobList() {
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  // Mock query - replace with actual API call
  const { data: jobs, isLoading, refetch } = useQuery(
    ['jobs', selectedStatus, searchQuery],
    () => {
      // Simulate API delay
      return new Promise((resolve) => {
        setTimeout(() => {
          let filteredJobs = mockJobs
          
          if (selectedStatus !== 'all') {
            filteredJobs = filteredJobs.filter(job => job.status === selectedStatus)
          }
          
          if (searchQuery) {
            filteredJobs = filteredJobs.filter(job => 
              job.query.toLowerCase().includes(searchQuery.toLowerCase())
            )
          }
          
          resolve(filteredJobs)
        }, 500)
      })
    },
    {
      refetchInterval: 5000, // Refetch every 5 seconds for real-time updates
    }
  )

  const getStatusConfig = (status: string) => {
    return statusConfig[status as keyof typeof statusConfig] || statusConfig.pending
  }

  const handleViewJob = (jobId: string) => {
    console.log('View job:', jobId)
    // Navigate to job detail page
  }

  const handleDeleteJob = (jobId: string) => {
    console.log('Delete job:', jobId)
    // Show confirmation dialog and delete job
  }

  const handleRefresh = () => {
    refetch()
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span className="ml-2 text-gray-600 dark:text-gray-400">Loading jobs...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Filters and Search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search jobs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field"
          />
        </div>
        <div className="flex gap-2">
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="input-field w-auto"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="planning">Planning</option>
            <option value="retrieving">Retrieving</option>
            <option value="synthesizing">Synthesizing</option>
            <option value="drafting">Drafting</option>
            <option value="fact_checking">Fact Checking</option>
            <option value="visualizing">Visualizing</option>
            <option value="reviewing">Reviewing</option>
            <option value="formatting">Formatting</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
          <button
            onClick={handleRefresh}
            className="btn-secondary"
          >
            <ArrowPathIcon className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Job List */}
      <div className="space-y-4">
        {jobs?.map((job, index) => {
          const status = getStatusConfig(job.status)
          const StatusIcon = status.icon

          return (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="card p-6 hover:shadow-md transition-shadow duration-200"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <StatusIcon className="h-5 w-5 text-gray-400" />
                    <span className={`status-badge ${status.className}`}>
                      {status.label}
                    </span>
                    {job.status === 'completed' && job.completedAt && (
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {formatDistanceToNow(job.completedAt, { addSuffix: true })}
                      </span>
                    )}
                  </div>
                  
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2 truncate">
                    {job.query}
                  </h3>
                  
                  <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                    <span>Created {formatDistanceToNow(job.createdAt, { addSuffix: true })}</span>
                    <span>•</span>
                    <span className="uppercase">{job.outputFormat}</span>
                    {job.status !== 'completed' && job.status !== 'failed' && (
                      <>
                        <span>•</span>
                        <span>{job.progress}% complete</span>
                      </>
                    )}
                  </div>

                  {/* Progress Bar */}
                  {job.status !== 'completed' && job.status !== 'failed' && (
                    <div className="mt-3">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${job.progress}%` }}
                        />
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 ml-4">
                  <button
                    onClick={() => handleViewJob(job.id)}
                    className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    title="View job"
                  >
                    <EyeIcon className="h-5 w-5" />
                  </button>
                  {job.status === 'completed' && (
                    <button
                      className="p-2 text-gray-400 hover:text-green-600 dark:hover:text-green-400 transition-colors"
                      title="Download report"
                    >
                      <DocumentTextIcon className="h-5 w-5" />
                    </button>
                  )}
                  <button
                    onClick={() => handleDeleteJob(job.id)}
                    className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                    title="Delete job"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </motion.div>
          )
        })}

        {jobs?.length === 0 && (
          <div className="text-center py-12">
            <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
              No jobs found
            </h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {searchQuery || selectedStatus !== 'all' 
                ? 'Try adjusting your search or filters.'
                : 'Get started by creating your first research job.'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
