import { forwardRef, type InputHTMLAttributes } from 'react'
interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> { label: string; error?: string }
export const FormField = forwardRef<HTMLInputElement, FormFieldProps>(function FormField({ label, error, id, ...props }, ref) {
  return <label className="form-field" htmlFor={id}><span>{label}</span><input ref={ref} id={id} aria-invalid={Boolean(error)} aria-describedby={error ? `${id}-error` : undefined} {...props} />{error && <small id={`${id}-error`} role="alert">{error}</small>}</label>
})
