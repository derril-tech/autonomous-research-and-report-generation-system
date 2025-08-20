'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { motion } from 'framer-motion'
import { 
  MagnifyingGlassIcon,
  DocumentTextIcon,
  ChartBarIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

const jobSchema = z.object({
  query: z.string().min(10, 'Query must be at least 10 characters'),
  constraints: z.object({
    region: z.string().optional(),
    dateRange: z.object({
      start: z.string().optional(),
      end: z.string().optional(),
    }).optional(),
    industries: z.array(z.string()).optional(),
    sources: z.array(z.string()).optional(),
    excludeSources: z.array(z.string()).optional(),
  }).optional(),
  output: z.object({
    format: z.enum(['pdf', 'docx', 'pptx']).default('pdf'),
    length: z.enum(['short', 'medium', 'long']).default('medium'),
    tone: z.enum(['academic', 'business', 'casual']).default('business'),
  }).default({
    format: 'pdf',
    length: 'medium',
    tone: 'business',
  }),
  hil: z.object({
    planGate: z.boolean().default(true),
    finalGate: z.boolean().default(true),
  }).default({
    planGate: true,
    finalGate: true,
  }),
})

type JobFormData = z.infer<typeof jobSchema>

export function JobCreationForm() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [activeStep, setActiveStep] = useState(1)

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<JobFormData>({
    resolver: zodResolver(jobSchema),
    defaultValues: {
      output: {
        format: 'pdf',
        length: 'medium',
        tone: 'business',
      },
      hil: {
        planGate: true,
        finalGate: true,
      },
    },
  })

  const watchedFormat = watch('output.format')
  const watchedLength = watch('output.length')
  const watchedTone = watch('output.tone')

  const onSubmit = async (data: JobFormData) => {
    setIsSubmitting(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      console.log('Job data:', data)
      toast.success('Research job created successfully!')
      
      // Reset form
      setValue('query', '')
      setActiveStep(1)
    } catch (error) {
      toast.error('Failed to create research job')
      console.error('Error creating job:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const steps = [
    { id: 1, name: 'Query', icon: MagnifyingGlassIcon },
    { id: 2, name: 'Constraints', icon: Cog6ToothIcon },
    { id: 3, name: 'Output', icon: DocumentTextIcon },
    { id: 4, name: 'Review', icon: ChartBarIcon },
  ]

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Steps */}
      <nav aria-label="Progress" className="mb-8">
        <ol className="flex items-center">
          {steps.map((step, stepIdx) => (
            <li
              key={step.name}
              className={`${
                stepIdx !== steps.length - 1 ? 'pr-8 sm:pr-10' : ''
              } relative`}
            >
              <div className="flex items-center">
                <div
                  className={`${
                    activeStep >= step.id
                      ? 'bg-primary-600 border-primary-600'
                      : 'bg-white border-gray-300 dark:bg-gray-800 dark:border-gray-600'
                  } relative flex h-8 w-8 items-center justify-center rounded-full border-2 transition-colors`}
                >
                  <step.icon
                    className={`${
                      activeStep >= step.id
                        ? 'text-white'
                        : 'text-gray-500 dark:text-gray-400'
                    } h-4 w-4 transition-colors`}
                    aria-hidden="true"
                  />
                </div>
                {stepIdx !== steps.length - 1 && (
                  <div
                    className={`${
                      activeStep > step.id
                        ? 'bg-primary-600'
                        : 'bg-gray-300 dark:bg-gray-600'
                    } absolute top-4 left-8 -ml-px h-0.5 w-8 transition-colors`}
                  />
                )}
              </div>
              <span className="sr-only">{step.name}</span>
            </li>
          ))}
        </ol>
      </nav>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Step 1: Query */}
        {activeStep === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-6"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              What would you like to research?
            </h3>
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Research Query
              </label>
              <textarea
                {...register('query')}
                id="query"
                rows={4}
                className="input-field"
                placeholder="Describe your research topic in detail. For example: 'Analyze the impact of artificial intelligence on healthcare delivery in the United States over the past 5 years, including adoption rates, cost savings, and patient outcomes.'"
              />
              {errors.query && (
                <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                  {errors.query.message}
                </p>
              )}
            </div>
            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => setActiveStep(2)}
                className="btn-primary"
                disabled={!watch('query') || watch('query').length < 10}
              >
                Next: Constraints
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 2: Constraints */}
        {activeStep === 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-6"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Add any constraints or preferences
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="region" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Geographic Region (optional)
                </label>
                <input
                  {...register('constraints.region')}
                  type="text"
                  id="region"
                  className="input-field"
                  placeholder="e.g., North America, Europe, Asia"
                />
              </div>
              <div>
                <label htmlFor="industries" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Industries (optional)
                </label>
                <input
                  {...register('constraints.industries')}
                  type="text"
                  id="industries"
                  className="input-field"
                  placeholder="e.g., Healthcare, Technology, Finance"
                />
              </div>
            </div>
            <div className="mt-6 flex justify-between">
              <button
                type="button"
                onClick={() => setActiveStep(1)}
                className="btn-secondary"
              >
                Back
              </button>
              <button
                type="button"
                onClick={() => setActiveStep(3)}
                className="btn-primary"
              >
                Next: Output Settings
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 3: Output Settings */}
        {activeStep === 3 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-6"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Configure output settings
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Format
                </label>
                <select
                  {...register('output.format')}
                  className="input-field"
                >
                  <option value="pdf">PDF</option>
                  <option value="docx">Word Document</option>
                  <option value="pptx">PowerPoint</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Length
                </label>
                <select
                  {...register('output.length')}
                  className="input-field"
                >
                  <option value="short">Short (2-3 pages)</option>
                  <option value="medium">Medium (5-7 pages)</option>
                  <option value="long">Long (10+ pages)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Tone
                </label>
                <select
                  {...register('output.tone')}
                  className="input-field"
                >
                  <option value="academic">Academic</option>
                  <option value="business">Business</option>
                  <option value="casual">Casual</option>
                </select>
              </div>
            </div>
            <div className="mt-6 flex justify-between">
              <button
                type="button"
                onClick={() => setActiveStep(2)}
                className="btn-secondary"
              >
                Back
              </button>
              <button
                type="button"
                onClick={() => setActiveStep(4)}
                className="btn-primary"
              >
                Next: Review
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 4: Review */}
        {activeStep === 4 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-6"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Review your research request
            </h3>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Query</h4>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  {watch('query')}
                </p>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Output Settings</h4>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  {watchedFormat.toUpperCase()} • {watchedLength} • {watchedTone}
                </p>
              </div>
              {watch('constraints.region') && (
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Region</h4>
                  <p className="text-gray-600 dark:text-gray-300 mt-1">
                    {watch('constraints.region')}
                  </p>
                </div>
              )}
            </div>
            <div className="mt-6 flex justify-between">
              <button
                type="button"
                onClick={() => setActiveStep(3)}
                className="btn-secondary"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn-primary"
              >
                {isSubmitting ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Creating...
                  </div>
                ) : (
                  'Create Research Job'
                )}
              </button>
            </div>
          </motion.div>
        )}
      </form>
    </div>
  )
}
