<script setup lang="ts">
</script>

<template>
    <div class="help-container">
        <h1>welcome to simple dash</h1>
        <p class="subtitle">Usability-focused email campaign analytics that helps you visualize and compare your
            marketing performance</p>

        <section class="help-section">
            <div class="value-props">
                <div class="value-prop">
                    <div class="icon">📊</div>
                    <h3>Instant Insights</h3>
                    <p>Upload your campaign reports and instantly see trends, metrics, and performance comparisons.</p>
                </div>
                <div class="value-prop">
                    <div class="icon">🔒</div>
                    <h3>Privacy First</h3>
                    <p>Files immediately discarded after being parsed. No campaign data is permanently stored on our
                        servers.</p>
                </div>
                <div class="value-prop">
                    <div class="icon">🚀</div>
                    <h3>No Setup Required</h3>
                    <p>No accounts needed. Just upload your CSV reports and view your dashboard
                        instantly.</p>
                </div>
            </div>
        </section>

        <section class="help-section">
            <h2>How It Works</h2>

            <div class="step">
                <h3>Step 1: Upload Your Reports</h3>
                <p>Export your campaign reports as CSV files from your email marketing platform (MailChimp or
                    MailerLite Classic).</p>
            </div>

            <div class="step">
                <h3>Step 2: Automatic Parsing</h3>
                <p>Our parser automatically detects your platform and extracts key metrics like open rates, click
                    rates, bounces, and more.</p>
            </div>

            <div class="step">
                <h3>Step 3: View Your Dashboard</h3>
                <p>Explore individual campaign performance or view trends across all your campaigns with interactive
                    charts and visualizations.</p>
            </div>
        </section>

        <section class="help-section">
            <h2>Supported Platforms</h2>
            <div class="platforms-grid">
                <div class="platform-card">
                    <h3>MailChimp</h3>
                    <p>Export your individual, A/B test, or aggregated campaign reports as CSV files from the MailChimp
                        audience. If a campaign is in multiple reports (based on unique ID), the metrics from the most
                        recent
                        upload will be used.</p>
                </div>
                <div class="platform-card">
                    <h3>MailerLite Classic</h3>
                    <p>Export campaign reports from MailerLite Classic in CSV format.</p>
                </div>
            </div>
            <p class="platforms-note">
                <em>More platforms coming soon!</em>
            </p>
        </section>

        <section class="help-section privacy-box">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" class="privacy-icon">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
            <div>
                <h2>Your Data Stays Private</h2>
                <ul>
                    <li><strong>No persistent storage:</strong> Your CSV files are sent to the server for parsing, but
                        are immediately discarded after processing. No campaign data is stored on the server.</li>
                    <li><strong>Local browser storage only:</strong> Parsed campaign data is returned to your browser
                        and stored temporarily in session storage.</li>
                    <li><strong>Cleared when you leave:</strong> All data is automatically cleared when you close the
                        tab or navigate away.</li>
                    <li><strong>No accounts or tracking:</strong> No sign-up required, no cookies, no tracking.</li>
                </ul>
            </div>
        </section>

        <section class="help-section">
            <h2>File Requirements</h2>
            <ul>
                <li><strong>Format:</strong> CSV files only</li>
                <li><strong>Maximum file size:</strong> 10MB per file</li>
                <li><strong>Maximum files:</strong> 12 files per upload</li>
                <li><strong>Platform detection:</strong> Automatic (MailChimp and MailerLite Classic formats
                    recognized)</li>
            </ul>
        </section>

        <section class="help-section">
            <h2>Tips for Best Results</h2>
            <ul>
                <li>Upload multiple campaigns to unlock trend analysis and the send-time heatmap</li>
                <li>Make sure your CSV files are exported directly from your email platform without
                    modifications
                </li>
                <li>Campaign data is sorted chronologically by send date for accurate trend visualization</li>
                <li>If some files fail to parse, successfully parsed campaigns will still be displayed with a
                    warning banner</li>
                <li>For MailChimp: Duplicate campaigns (same unique ID) across multiple files will be
                    automatically
                    deduplicated, keeping the version from the most recent upload</li>
            </ul>
        </section>

        <section class="help-section">
            <h2>FAQ</h2>

            <div class="faq-item">
                <h3>My file failed to upload</h3>
                <p>Make sure your file is a valid CSV file from MailChimp or MailerLite Classic, under 10MB in size, and
                    not modified or corrupted.</p>
            </div>

            <div class="faq-item">
                <h3>I don't see my data on the dashboard</h3>
                <p>This can happen if all uploaded files failed to parse (check for error messages), you're using a
                    private/incognito window with session storage disabled, or your browser doesn't support session
                    storage.</p>
            </div>

            <div class="faq-item">
                <h3>Can I export or save my dashboard?</h3>
                <p>Currently, Simple Dash doesn't offer export functionality. You can take screenshots of your dashboard
                    or re-upload your files anytime to view the data again.</p>
            </div>

            <div class="faq-item">
                <h3>How long is my data stored?</h3>
                <p>Your campaign data is only stored in your browser's session storage and is automatically cleared when
                    you close the tab or navigate away. The server does not retain any data after parsing.</p>
            </div>

            <div class="faq-item">
                <h3>What if I have campaigns from different platforms?</h3>
                <p>You can upload CSV files from multiple platforms in the same session. The parser will automatically
                    detect and handle each platform's format independently.</p>
            </div>
        </section>

        <section class="help-section connect-section">
            <div class="connect-header">
                <h2>Have an Idea for a Tool?</h2>
            </div>
            <p class="connect-text">
                Are you a marketer, founder, or business owner with an idea for a tool that could solve real-world
                problems?
            </p>
            <p class="connect-text">
                I built Simple Dash to help marketers analyze their email campaigns more effectively. If you have a pain
                point that could be solved with a tool like this, I'd love to hear about it!
            </p>
            <a href="https://www.linkedin.com/in/derekology" target="_blank" rel="noopener" class="linkedin-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="button-icon">
                    <path
                        d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                </svg>
                Connect on LinkedIn
            </a>
        </section>

        <section class="help-section disclaimer-section">
            <h2>Disclaimer</h2>
            <p class="disclaimer-text">
                Simple Dash is provided "as-is" without any warranties or guarantees of any kind, express or
                implied. The developers and maintainers are not responsible for any data loss, parsing errors,
                service interruptions, or any other issues that may arise from using this tool. Use at your own risk.
            </p>
            <p class="disclaimer-text">
                While your CSV files are sent to the server for parsing and immediately discarded afterward with no
                persistent storage, you are responsible for ensuring your use of this tool complies with all applicable
                data privacy laws and regulations in your jurisdiction. Always handle campaign data in accordance with
                your organization's privacy policies and applicable laws.
            </p>
            <p class="disclaimer-text">
                This tool is intended for legitimate analytics and campaign monitoring purposes. The developers
                assume no liability for how users choose to use Simple Dash or the decisions made based on the
                analytics provided.
            </p>
        </section>
    </div>
</template>

<style scoped>
.help-container {
    padding: var(--spacing-xl);
    max-width: 1000px;
    margin: 0 auto;
    min-height: calc(100vh - var(--top-bar-height));
}

.help-container h1 {
    font-size: 2.5rem;
    color: var(--color-text);
    margin-bottom: var(--spacing-sm);
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: var(--color-text-light);
    margin-bottom: var(--spacing-xl);
}

.help-section {
    background: var(--color-bg-white);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
    box-shadow: var(--shadow-md);
}

.help-section h2 {
    font-size: 1.8rem;
    margin: 0 0 var(--spacing-lg) 0;
    padding-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.help-section h3 {
    font-size: 1.3rem;
    margin: 0 0 0.75rem 0;
}

.help-section p {
    font-size: var(--spacing-md);
    line-height: 1.6;
    color: var(--color-text-light);
    margin-bottom: var(--spacing-md);
}

.help-section ul {
    margin: var(--spacing-sm) 0 0 var(--spacing-lg);
    color: var(--color-text-light);
    line-height: 1.8;
}

.help-section ul li {
    margin-bottom: var(--spacing-sm);
}

.value-props {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
}

.value-prop {
    text-align: center;
    padding: var(--spacing-md);
}

.value-prop .icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-sm);
}

.value-prop h3 {
    font-size: 1.2rem;
    color: var(--color-text);
    margin: var(--spacing-sm) 0;
}

.value-prop p {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--color-text-light);
    margin: 0;
}

.step {
    margin-bottom: var(--spacing-xl);
}

.step:last-child {
    margin-bottom: 0;
}

.platforms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
}

.platform-card {
    padding: var(--spacing-lg);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-lg);
}

.platform-card h3 {
    margin-bottom: var(--spacing-sm);
}

.platform-card p {
    margin: 0;
    font-size: 0.95rem;
    color: var(--color-text-light);
}

.platforms-note {
    text-align: center;
    color: var(--color-text-lighter);
    font-size: 0.9rem;
}

.privacy-box {
    display: flex;
    gap: var(--spacing-lg);
    background: var(--color-bg-info-gradient);
    border-left: 5px solid var(--color-info);
}

.privacy-icon {
    width: 48px;
    height: 48px;
    color: var(--color-info);
    flex-shrink: 0;
}

.privacy-box h3 {
    margin-bottom: var(--spacing-md);
}

.privacy-box ul {
    margin: 0;
    padding-left: var(--spacing-lg);
}

.privacy-box li {
    margin-bottom: var(--spacing-sm);
    line-height: 1.6;
}

.faq-item {
    margin-bottom: var(--spacing-lg);
}

.faq-item:last-child {
    margin-bottom: 0;
}

.faq-item h3 {
    font-size: 1.1rem;
    color: var(--color-text);
    margin: 0 0 var(--spacing-sm) 0;
}

.faq-item p {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--color-text-light);
}

.disclaimer-section {
    border-left: 5px solid var(--color-text-light);
}

.disclaimer-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--color-text-light);
    margin: 0 0 var(--spacing-md) 0;
}

.disclaimer-text:last-child {
    margin-bottom: 0;
}

.connect-section {
    background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
    color: #ffffff;
    border: none;
    padding: var(--spacing-xl);
    text-align: center;
}

.connect-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
}

.connect-header h2 {
    color: #ffffff;
    margin: 0;
}

.connect-section .connect-text {
    font-size: 1rem;
    line-height: 1.7;
    color: #ffffff;
    margin: 0 0 var(--spacing-md) 0;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.connect-text strong {
    font-weight: 700;
}

.linkedin-button {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-xl);
    background-color: #ffffff;
    color: #0077b5;
    text-decoration: none;
    border-radius: var(--radius-lg);
    font-weight: 700;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    margin-top: var(--spacing-md);
}

.linkedin-button:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    background-color: #f8f9fa;
}

.button-icon {
    width: 24px;
    height: 24px;
}

@media (max-width: 768px) {
    .help-container {
        padding: var(--spacing-md);
    }

    .help-container h1 {
        font-size: 2rem;
    }

    .value-props,
    .platforms-grid {
        grid-template-columns: 1fr;
    }

    .privacy-box {
        flex-direction: column;
        align-items: center;
    }
}
</style>
