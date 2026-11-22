import {
  Badge,
  Bar,
  Icon,
  LockScreen,
  Notification,
  Phone,
  Stage,
  Text,
  Window,
  type Act,
} from '../stageshow/kit'
import './notification-story.css'

type StoryState = {
  active: 0 | 1 | 2
  notification: boolean
}

const initial: StoryState = { active: 0, notification: false }
const poster: StoryState = { active: 2, notification: true }

async function script(a: Act<StoryState>) {
  await a.wait(700)
  await a.set({ active: 1 })
  await a.wait(900)
  await a.set({ active: 2 })
  await a.wait(450)
  await a.set({ notification: true })
  await a.wait(2400)
  await a.set({ notification: false })
  await a.wait(300)
  await a.set(initial)
}

const events = [
  { name: 'order.completed', channel: 'Email', status: 'Received' },
  { name: 'invoice.overdue', channel: 'Push', status: 'Matched' },
  { name: 'payment.received', channel: 'Push', status: 'Sent' },
] as const

export function NotificationStory() {
  return (
    <Stage
      width={680}
      height={430}
      compact={{ below: 620, width: 358, height: 410 }}
      initial={initial}
      poster={poster}
      script={script}
      className="notification-story"
      tokens={{
        '--ss-accent': '#157a63',
        '--ss-accent-soft': '#dcefe9',
        '--ss-radius-md': '7px',
        '--ss-radius-window': '14px',
      }}
    >
      {(state) => (
        <>
          <Window title="Production" className="story-window">
            <aside className="story-sidebar">
              <Text className="story-wordmark">Relay</Text>
              {['Overview', 'Events', 'Rules', 'Deliveries'].map((item, index) => (
                <div className="story-nav-item" data-active={index === 1 || undefined} key={item}>
                  <Bar w={12} h={12} r={4} tone={index === 1 ? 5 : 2} />
                  <Text>{item}</Text>
                </div>
              ))}
            </aside>

            <section className="story-main">
              <header className="story-header">
                <div>
                  <Text className="story-title">Live events</Text>
                  <Text className="story-subtitle">Production environment</Text>
                </div>
                <Badge tone="success">All systems operational</Badge>
              </header>

              <div className="story-metrics">
                <div><Text>Delivered today</Text><strong>12,480</strong></div>
                <div><Text>Success rate</Text><strong>99.8%</strong></div>
                <div><Text>Median latency</Text><strong>184ms</strong></div>
              </div>

              <div className="event-list">
                <div className="event-head"><span>Event</span><span>Channel</span><span>Status</span></div>
                {events.map((event, index) => {
                  const reached = state.active >= index
                  return (
                    <div className="event-row" data-active={state.active === index || undefined} key={event.name}>
                      <div className="event-name"><span className="event-pulse" data-on={reached || undefined} /><code>{event.name}</code></div>
                      <span>{event.channel}</span>
                      <Badge tone={reached ? 'success' : 'neutral'}>{reached ? event.status : 'Queued'}</Badge>
                    </div>
                  )
                })}
              </div>
            </section>
          </Window>

          <Phone width={238} frame="pro" dark className="story-phone">
            <LockScreen size="satellite" stack="top">
              <div className="story-notification" data-show={state.notification || undefined}>
                <Notification
                  icon={<Icon name="bolt" filled size={20} />}
                  title="Payment received"
                  body="Your payment of $249.00 was confirmed."
                />
              </div>
            </LockScreen>
          </Phone>
        </>
      )}
    </Stage>
  )
}
